from fastapi import FastAPI, status

from src.db import create_post, get_single_post, get_all_posts, get_all_users, get_single_user
from src.schemas import NewPostSchema, JsonApiResponseSchema, PostSchema, UserSchema

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/post/new/", status_code=status.HTTP_201_CREATED)
async def new_post(post: NewPostSchema) -> JsonApiResponseSchema:
    obj = create_post(post)
    (obj, nr_likes) = get_single_post(obj.id)
    payload = PostSchema(
        id=obj.id,
        author_id=obj.author_id,
        content=obj.content,
        nr_likes=nr_likes,
    )
    resp = JsonApiResponseSchema(data=payload)
    return resp


@app.get("/post/")
async def all_posts() -> JsonApiResponseSchema:
    posts = get_all_posts()
    payload = [
        PostSchema(
            id=post.id,
            author_id=post.author_id,
            content=post.content,
            nr_likes=nr_likes,
        )
        for (post, nr_likes) in posts
    ]
    resp = JsonApiResponseSchema(data=payload)
    return resp


@app.get("/post/{{post_id}}")
async def single_post(post_id: int) -> JsonApiResponseSchema:
    resp = JsonApiResponseSchema()
    (post, nr_likes) = get_single_post(post_id)
    if post:
        resp.data = PostSchema(
            id=post.id,
            author_id=post.author_id,
            content=post.content,
            nr_likes=nr_likes,
        )
    else:
        resp.errors = [f"no post found with id={post_id}"]
    return resp


@app.get(f"/user/")
async def all_users() -> JsonApiResponseSchema:
    users = get_all_users()
    payload = [
        UserSchema(
            id=user.id,
            username=user.username,
            email=user.email,
        )
        for user in users
    ]
    resp = JsonApiResponseSchema(data=payload)
    return resp


@app.get(f"/user/{{user_id}}")
async def single_user(user_id: int) -> JsonApiResponseSchema:
    resp = JsonApiResponseSchema()
    user = get_single_user(user_id)
    if user:
        resp.data = UserSchema(
            id=user.id,
            username=user.username,
            email=user.email,
        )
    else:
        resp.errors = [f"no user found with id={user_id}"]
    return resp
