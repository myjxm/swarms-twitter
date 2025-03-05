from langchain_community.document_loaders import TextLoader
# from langchain_community.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


class RagAssistant:
    def __init__(
            self,
            persist_directory:str='twitter_knowledge',
    ):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.db=Chroma(persist_directory=persist_directory, embedding_function=self.embeddings)

    def add_contents(self,texts:list,metadatas:list):
        self.db.add_texts(texts, embedding=self.embeddings, metadatas=metadatas)
        self.db.persist()
        return  {"code":0,"message":"Successfully added contents in db"}

    def search_by_metadata(self,metadata:dict):
        results = self.db.similarity_search_with_score("", filter=metadata)
        return results

    ### 基于 metadata 删除
    def delete_by_metadata(self,target_metadata:dict):
        # 获取满足 metadata 条件的文档的 ID
        ids_to_delete = []
        results = self.db.similarity_search_with_score("", filter=target_metadata)
        for doc, _ in results:
            # 假设文档有唯一的 ID 存储在 metadata 中，如果没有可以根据实际情况调整
            doc_id = doc.metadata.get('id')
            if doc_id:
                ids_to_delete.append(doc_id)
        # 根据 ID 删除文档
        if ids_to_delete:
            result = self.db.delete(where=target_metadata)
            #self.db.delete(ids=ids_to_delete)
            # 持久化数据库以保存删除操作
            self.db.persist()
            return f"已删除 {len(ids_to_delete)} 条记录"
        else:
            return "未找到符合条件的记录"

    ### 基于 metadata 更新
    def update_by_metadata(self,target_metadata, new_text, new_metadata):
        # 获取满足 metadata 条件的文档的 ID
        ids_to_update = []
        results = self.db.similarity_search_with_score("", filter=target_metadata)
        for doc, _ in results:
            doc_id = doc.metadata.get('id')
            if doc_id:
                ids_to_update.append(doc_id)
        # 删除旧的文档
        if ids_to_update:
            self.db.delete(ids=ids_to_update)
        # 添加新的文档
        self.db.add_texts([new_text], metadatas=[new_metadata])
        # 持久化数据库以保存更新操作
        self.db.persist()
        return "已更新记录"






