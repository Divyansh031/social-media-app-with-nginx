from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from typing import List, Optional
from ..import schemas, models, oauth2
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])  # Create a router for post-related endpoints

# POST Endpoints

@router.get("/", response_model=List[schemas.Post]) # Retrieve all posts and return them as a list of Post schemas
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):  # Retrieve all posts
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts   

@router.post("/", response_model=schemas.Post)
def create_posts(post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): # Create a new post using the Post model
    new_post = models.Post(**post.dict(), owner_id=current_user.id)  # Create a new Post instance **post.dict() converts the Pydantic model to a dictionary 
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # Refresh the instance to get the updated data from the database
    return new_post # Return the post data as a response



@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} was not found") # Raise an error if post not found
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id==id)
    
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")

    post_query.delete(synchronize_session=False)  # Delete the post
    db.commit()


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first() # This just gets the query object, not the actual post
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")
    
    post_query.update(updated_post.dict(), synchronize_session=False) # synchronize_session=False means we don't need to update the session after this operation
    db.commit()
    return post_query.first()
    