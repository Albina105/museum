import asyncio
from fastapi import APIRouter, HTTPException
from langchain_core.exceptions import OutputParserException
from mysite.chain.museum_chain import museum_chain
from mysite.base_knowledge.museum_knowledge import museum_documents
from mysite.schemas.ai_schema import AskInputSchema, AskOutputSchema

ai_router = APIRouter(prefix='/ai', tags=['AI Guide'])


@ai_router.post(path='/ask', response_model=AskOutputSchema)
async def ask_guide(ask: AskInputSchema):
    question = ask.question.strip()

    if not question:
        raise HTTPException(status_code=422, detail='Данные переданы в неверном формате')

    context = '\n\n'.join(document.page_content for document in museum_documents)

    try:
        answer = await asyncio.wait_for(
            museum_chain.ainvoke({'question': question, 'context': context}), timeout=120
        )
    except TimeoutError:
        raise HTTPException(status_code=500, detail='Модель не успела выполнить задачу')
    except OutputParserException:
        raise HTTPException(status_code=500, detail='Ответ модели не подходит под схему')
    except Exception:
        raise HTTPException(status_code=500, detail='Ollama не отвечает, проверь что она запущена')

    return AskOutputSchema(answer=answer.strip())
