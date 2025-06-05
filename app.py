# R&R (Role and Responsibility) - 업무분장을 위한 역할분담 문서
# 도서관리 API + Swagger UI 
# GET / books : 조회
# POST / book : 등록
# 옵져버 패턴을 적용 새도서 추가 RAG 시스템의 검색 모듈에 알림
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from typing import List, Dict
import unicorn # Swagger UI를 지원하는 서버

# pydantic 모델 정의
class Book(BaseModel):
    id : int
    title : str

class BookCreate(BaseModel):
    title:str
books =[
    Book(id=1,title= 'llm study'),
    Book(id=2,title= 'python study')
]
# 옵져버 패턴 구현
class Subject:
    def __init__(self) -> None:
        self._observer = []
    def add_observer(self, obs):
        self._observer.append(obs)
    def notify(self, message):
        for obs in self._observer:
            obs.update(message)
class Observer:
    def update(self, message):
        raise NotImplementedError
# 옵져서... RAG 시스템의 검색메소드
class SearchModule(Observer):
    def update(self, message):
        return super().update(message, "인덱스 업데이터")
# BookManager (Subject):
class BookMnager(Subject):
    # 책추가
    def add_book(self, book:BookCreate):
        new_id = max(b.id for b in books) + 1
        new_books = Book(id = new_id, title = book.title)
        self.notify(f'새로운 도서 추가 : {new_books.title}')
book_manager = BookMnager()
search_module = SearchModule()
book_manager.add_observer(search_module)

app = FastAPI()
#호출
@app.get("/book", response_model = List[Book], tags = ['Books'])
def get_books():
    return books
@app.get("/book", response_model = List[Book], tags = ['Books'])
def Create_books():