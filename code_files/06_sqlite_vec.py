import sqlite3
from typing import Tuple, Optional, List, Any, Union, Iterable
import sqlite_vec 
from sqlite_vec import serialize_float32

class VectorDatabase:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None
        self._connect()
    
    def _connect(self) -> None:
        self.connection = sqlite3.connect(self.db_path)
        self.connection.enable_load_extension(True)
        sqlite_vec.load(self.connection)
        self.connection.enable_load_extension(False)
    
    def get_versions(self) -> Tuple[str, str]:
        if not self.connection:
            self._connect()
        return self.connection.execute(
            "SELECT sqlite_version(), vec_version()"
        ).fetchone()
    
    def display_version_info(self) -> None:
        sqlite_version, vec_version = self.get_versions()
        print(f"sqlite_version={sqlite_version}, vec_version={vec_version}")
    
    def execute(self, query: str, params: Union[tuple, dict, list, None] = None) -> sqlite3.Cursor:
        if not self.connection:
            self._connect()
            
        try:
            if params:
                return self.connection.execute(query, params)
            else:
                return self.connection.execute(query)
        except sqlite3.Error as e:
            print(f"Query execution error: {e}")
            raise
    
    def executemany(self, query: str, params_seq: Iterable[Union[tuple, dict, list]]) -> sqlite3.Cursor:
        if not self.connection:
            self._connect()
            
        try:
            return self.connection.executemany(query, params_seq)
        except sqlite3.Error as e:
            print(f"Query execution error: {e}")
            raise
    
    def execute_fetchall(self, query: str, params: Union[tuple, dict, list, None] = None) -> List[tuple]:
        cursor = self.execute(query, params)
        return cursor.fetchall()
    
    def execute_fetchone(self, query: str, params: Union[tuple, dict, list, None] = None) -> Optional[tuple]:
        cursor = self.execute(query, params)
        return cursor.fetchone()
    
    def create_vector_table(self, table_name: str, dimensions: int) -> None:
        self.execute(f"CREATE VIRTUAL TABLE IF NOT EXISTS {table_name} USING vec0(embedding float[{dimensions}])")
    
    def commit(self) -> None:
        if self.connection:
            self.connection.commit()
    
    def close(self) -> None:
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection and exc_type is None:
            self.connection.commit()
        self.close()


# def serialize_float32(vector: List[float]) -> bytes:
#     return struct.pack(f'{len(vector)}f', *vector)


def find_similar_vectors(db: VectorDatabase, table_name: str, query_vector: List[float], limit: int = 3) -> List[tuple]:
    return db.execute_fetchall(
        f"""
        SELECT
          rowid,
          distance
        FROM {table_name}
        WHERE embedding MATCH ?
        ORDER BY distance
        LIMIT ?
        """,
        [serialize_float32(query_vector), limit]
    )


def load_vectors(db: VectorDatabase, table_name: str, items: List[Tuple[int, List[float]]]) -> None:
    serialized_items = [(item[0], serialize_float32(item[1])) for item in items]
    
    with db:
        for item_id, serialized_vector in serialized_items:
            db.execute(
                f"INSERT INTO {table_name}(rowid, embedding) VALUES (?, ?)",
                [item_id, serialized_vector]
            )


def main():
    items = [
        (1, [0.1, 0.1, 0.1, 0.1]),
        (2, [0.2, 0.2, 0.2, 0.2]),
        (3, [0.3, 0.3, 0.3, 0.3]),
        (4, [0.4, 0.4, 0.4, 0.4]),
        (5, [0.5, 0.5, 0.5, 0.5]),
    ]
    query_vector = [0.3, 0.3, 0.3, 0.3]
    table_name = "vec_data"
    vector_dimensions = 4
    
    with VectorDatabase("local.sqlite") as db:
        db.display_version_info()

        # uncomment below lines when creating the table

        # db.create_vector_table(table_name, vector_dimensions)
        # load_vectors(db, table_name, items)
        similar_vectors = find_similar_vectors(db, table_name, query_vector)
        
        print("\n\nInserted embeddings:")
        for row in items:
            print(row)
        print("\nQuery Vector:")
        print(query_vector)

        

        print("\nSimilar vectors found:")
        print("----------------------")
        for row_id, distance in similar_vectors:
            print(f"ID: {row_id}, Distance: {distance}")
        

        print('\n\n'+"="*20 +"Distance Metrics" + "="*20)
        print("\nL2 (Euclidean Distance) and Cosine Distance:")
        custom_results = db.execute_fetchall(
            f"""
            SELECT 
                a.rowid AS vector1_id,
                b.rowid AS vector2_id,
                vec_distance_l2(a.embedding, b.embedding) AS l2_distance,
                vec_distance_cosine(a.embedding, b.embedding) AS cosine_distance
            FROM {table_name} a
            CROSS JOIN {table_name} b
            WHERE a.rowid < b.rowid
            ORDER BY a.rowid, b.rowid
            LIMIT 6
            """
        )
        for row in custom_results:
            print(row)


if __name__ == "__main__":
    main()



"""
When to Use This
`sqlite-vec `is perfect when:

- You want lightweight, embedded vector search
- You already use SQLite and want to avoid external dependencies
- You’re building AI-powered apps on the edge or mobile
- You want reproducible, portable vector pipelines

It may not be ideal for large-scale distributed
search across millions of high-dimensional vectors,
but for local, embedded, or small-medium applications, it’s shockingly capable.

"""