from backend.rag import rag_answer


# Change role to test FGAC
role = "OPS"

question ="i want to know about our daily operation policy?"

answer = rag_answer(question, role)
print("ANSWER:\n", answer)
