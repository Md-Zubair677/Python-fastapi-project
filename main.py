from fastapi import FastAPI, Request, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
#for error handling and validation error handling
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

# importing the schemas from pydantic models for request body validation
from schemas import PostCreate, PostResponse


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

posts: list[dict] = [
    {
        "id": 1,
        "author": "Corey Schafer",
        "title": "FastAPI is Awesome",
        "content": "This framework is really easy to use and super fast.",
        "date_posted": "April 20, 2025",
    },
    {
        "id": 2,
        "author": "Jane Doe",
        "title": "Python is Great for Web Development",
        "content": "Python is a great language for web development, and FastAPI makes it even better.",
        "date_posted": "April 21, 2025",
    },
]


@app.get("/", include_in_schema=False, name="home")
@app.get("/home", include_in_schema=False)
@app.get("/posts", include_in_schema=False, name="posts")
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "home.html",
        {"posts": posts, "title": "Home"},
    )

# This endpoint retrieves a single post by its ID and renders it using the post.html template
# It iterates through the posts list to find a matching post ID
# If found, it returns a template response with the post data and title
# If no matching post is found, it raises a 404 HTTP exception

@app.get("/posts/{post_id}", include_in_schema=False)
def get_post1(request: Request,post_id: int):
    for post in posts:
        if post["id"]==post_id:
            return templates.TemplateResponse(
                request,
                "post.html",
                {"post": post, "title": post["title"]},
            )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


# aap.gets helps to display the posts , reonse models checks all this posts
@app.get("/api/posts", response_model=list[PostResponse])
def get_posts():
    return posts

# creating a post
@app.post(
        "/api/posts",
        response_model=PostResponse,
        status_code=status.HTTP_201_CREATED,
)

def CreatePost(post: PostCreate):
    new_id = max(post["id"] for post in posts) + 1 if posts else 1
    new_post = {
        "id": new_id,
        "author": post.author,
        "title": post.title,
        "content": post.content,
        "date_posted": "06-06-2026",
    }
    posts.append(new_post)
    return new_post

@app.get("/api/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int):
    for post in posts:
        if post["id"] == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post in posts not found")

# exception handler for 404 errors giving a custom message for 404 errors and a generic message for other HTTP exceptions
@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exc: StarletteHTTPException):
   message = (
       exc.detail
       if exc.status_code != status.HTTP_404_NOT_FOUND
       else "The page you are looking for does not exist."
   )

   if request.url.path.startswith("/api/"):
       return JSONResponse(
           status_code=exc.status_code,
           content={"detail": message},
       )
   
   return templates.TemplateResponse(
       request,
       "error.html",
       {
           "status_code": exc.status_code,
           "title": f"Error {exc.status_code}",
           "message": message,
       },
       status_code=exc.status_code,
   )

#validation error handler for request body validation errors that occur when the incoming request data does not match the expected schema defined by Pydantic models.
@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exc.errors()},
        )
    
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "title": "Validation Error",
            "message": "The request data is invalid.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )







































































































































































































































































































































































































# from fastapi import FastAPI 
# from model import product

# app=FastAPI()
# @app.get("/")
# def greet():
#     return "hello this is the first msg of fast api"

# products = [
#     product(id=1, name="Mobile", des="Smartphone with 128GB storage", price=699.99),
#     product(id=2, name="Laptop", des="15-inch laptop with 16GB RAM", price=999.99),
#     product(id=3, name="Tablet", des="10-inch Android tablet", price=299.99),
#     product(id=4, name="Smartwatch", des="Fitness tracking smartwatch", price=199.99),
#     product(id=5, name="Headphones", des="Wireless noise-cancelling headphones", price=149.99),
#     product(id=6, name="Keyboard", des="Mechanical RGB keyboard", price=89.99),
#     product(id=7, name="Mouse", des="Wireless gaming mouse", price=59.99),
#     product(id=8, name="Monitor", des="24-inch Full HD monitor", price=179.99),
#     product(id=9, name="Speaker", des="Bluetooth portable speaker", price=79.99),
#     product(id=10, name="Camera", des="Digital camera with 4K recording", price=549.99)
# ]

# @app.get("/crd")

# def all_the_consumers():
#     return products

# @app.get("/product/{id}")
# def product_with_id(id:int):
#     for product in products:
#         if product.id==id:
#             return product
    

#     return "product not found"

# @app.post("/product")
# def adding_product(product: product):
#     products.append(product)

# @app.put("/product")
# def update_product(id:int, product : product):
#     for i in range(len(products)):
#        if products[i].id==id:
#            products[i]=product
#            return "sucessfully added the product"
    
#     return "no product added"

# @app.delete("/product")
# def delete_product(id:int):
#     for i in range(len(products)):
#         if products[i].id==id:
#             del products[i]