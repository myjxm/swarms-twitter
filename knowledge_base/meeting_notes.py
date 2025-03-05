from .rag_tools import RagAssistant
import uuid


class MeetingAssistant:
    def __init__(self):
        self.rag_assistant = RagAssistant()

    def save_meeting_notes(self,notes:list[dict]):
        texts = []
        metadatas = []
        for note in notes:
            texts.append(note["content"])
            metadatas.append({"id": uuid.uuid4().hex,"date": note["date"], "topic": note["topic"]})
        return self.rag_assistant.add_contents(texts,metadatas)

    def query_meeting_notes_by_metadata(self,metadatas:dict):
        # 直接从向量数据库中查询指定日期的文档
        results = self.rag_assistant.search_by_metadata(metadatas)
        return results


    def delete_meeting_notes_by_metadata(self,metadatas:dict):
        return self.rag_assistant.delete_by_metadata(metadatas)


if __name__ == "__main__":
    ma=MeetingAssistant()
    print(ma.query_meeting_notes_by_metadata({"date":'2025-02-25'}))