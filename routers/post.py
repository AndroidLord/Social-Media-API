from fastapi import APIRouter, status, Response, HTTPException, Depends
import models, schemas, oauth2
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


# CRUD Operations for Posts

# Create
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,
                 db: Session = Depends(get_db),
                 user_id: int = Depends(oauth2.get_current_user)):
    # example of using raw sql without SQLAlchemy
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",(new_post.title,new_post.content,new_post.published))
    # res = cursor.fetchone()
    # con.commit()

    # example of using SQLAlchemy
    new_post = models.Post(owner_id=user_id.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# Read

# Get All Posts
@router.get('/', response_model=list[schemas.Post])
def get_posts(db: Session = Depends(get_db),
              user_id: int = Depends(oauth2.get_current_user),
              limit: int = 10):

    # Example of how to get data from DB using SQLAlchemy
    posts = (db.query(models.Post)
         #    .filter(models.Post.owner_id == user_id.id)
             .limit(limit)
             .all())
    return posts


# Get Post by ID
@router.get('/{id}', response_model=schemas.Post)
def get_post(id: int,
             db: Session = Depends(get_db),
             user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id=%s""",(id,))
    #
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post:
        return post
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")


# Update
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
def update_post(id: int,
                post: schemas.PostCreate,
                db: Session = Depends(get_db),
                user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING *""",
    #                (new_post.title,new_post.content,new_post.published,id))
    # res = cursor.fetchone()
    # con.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    if post_query.first().owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User not authorized to update post")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()


# Delete
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_post(id: int,
                db: Session = Depends(get_db),
                user_id: int = Depends(oauth2.get_current_user)):
    # index = find_index_by_id(id)

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    if post.owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User not authorized to delete post")

    # cursor.execute("""DELETE FROM posts WHERE id=%s""",(id,))
    # con.commit()

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
