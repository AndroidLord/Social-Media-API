from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

import database, schemas, models, oauth2

router = APIRouter(
    prefix="/votes",
    tags=["votes"]
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(
        vote: schemas.Vote,
        db: Session = Depends(database.get_db),
        current_user: int = Depends(oauth2.get_current_user)):

    #Check if post exists
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'Post {vote.post_id} Does not exist')

    #Check if user has already voted
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id,
        models.Vote.user_id == current_user.id)

    # Querying the vote
    found_vote = vote_query.first()

    # If the vote is 1, then we are adding a vote
    if(vote.dir == 1):
        if(found_vote):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail = f'user {current_user.id} already voted on post {vote.post_id}')
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return{"message": "Successfully added vote"}

    # If the vote is 0, then we are removing a vote
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = 'Vote Does not exist')
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Successfully deleted vote"}