"""Starter DBMS interview question bank for the Voice Viva Coach.

Questions are original paraphrases of common DBMS interview topics. The
``key_points`` list is a lightweight rubric for answer feedback, not a
complete textbook definition.
"""

QUESTION_BANK = {
    "sql_basics": [
        {
            "id": "dbms_sql_001",
            "question": "What is the difference between a primary key and a unique key?",
            "key_points": [
                "A primary key uniquely identifies each row.",
                "A primary key cannot contain NULL values.",
                "A table has one primary-key constraint, which may contain multiple columns.",
                "A table can have multiple UNIQUE constraints; NULL handling depends on the database system.",
            ],
            "retry_question": "Can a table have more than one UNIQUE constraint, and can its primary key be NULL?",
            "difficulty": "beginner",
            "topic": "keys",
        },
        {
            "id": "dbms_sql_002",
            "question": "How are DELETE, TRUNCATE, and DROP different?",
            "key_points": [
                "DELETE removes selected rows and can use a WHERE clause.",
                "TRUNCATE removes all rows while keeping the table definition; transactional and identity behavior varies by DBMS.",
                "DROP removes the table object and its definition.",
            ],
            "retry_question": "Which command removes only matching rows, and which command removes the table itself?",
            "difficulty": "beginner",
            "topic": "sql",
        },
        {
            "id": "dbms_sql_003",
            "question": "What is the difference between WHERE and HAVING?",
            "key_points": [
                "WHERE filters rows before grouping and aggregation.",
                "HAVING filters groups after GROUP BY and aggregation.",
                "HAVING is commonly used with aggregate conditions such as COUNT or SUM.",
            ],
            "retry_question": "If you want to keep only departments with more than five employees, should the aggregate condition go in WHERE or HAVING?",
            "difficulty": "beginner",
            "topic": "sql",
        },
        {
            "id": "dbms_sql_004",
            "question": "Explain the difference between INNER JOIN and LEFT JOIN.",
            "key_points": [
                "INNER JOIN returns rows with matching join values on both sides.",
                "LEFT JOIN keeps every row from the left input.",
                "For unmatched left rows, right-side columns are returned as NULL.",
            ],
            "retry_question": "Which join still returns a customer who has no matching order?",
            "difficulty": "beginner",
            "topic": "joins",
        },
        {
            "id": "dbms_sql_005",
            "question": "What is a subquery, and when might you use one?",
            "key_points": [
                "A subquery is a query nested inside another SQL statement.",
                "It can provide a value or row set used by the outer query.",
                "Examples include filtering with IN or EXISTS, or comparing against an aggregate.",
            ],
            "retry_question": "How could a nested query help find employees whose salary is above the company average?",
            "difficulty": "beginner",
            "topic": "sql",
        },
        {
            "id": "dbms_sql_006",
            "question": "What is the difference between UNION and UNION ALL?",
            "key_points": [
                "Both combine compatible result sets vertically.",
                "UNION removes duplicate rows.",
                "UNION ALL preserves duplicates and is often less expensive because it skips duplicate elimination.",
            ],
            "retry_question": "Which one should you choose when duplicate rows must be preserved?",
            "difficulty": "beginner",
            "topic": "sql",
        },
    ],
    "normalization": [
        {
            "id": "dbms_norm_001",
            "question": "What is database normalization, and why is it used?",
            "key_points": [
                "Normalization organizes relational data into well-structured tables.",
                "It reduces unnecessary duplication and helps prevent update, insertion, and deletion anomalies.",
                "It uses normal forms and functional dependencies to guide decomposition.",
                "The design should still consider workload and performance trade-offs.",
            ],
            "retry_question": "Name one data anomaly that normalization can help prevent and briefly explain it.",
            "difficulty": "beginner",
            "topic": "normalization",
        },
        {
            "id": "dbms_norm_002",
            "question": "What conditions should a relation satisfy to be in First Normal Form (1NF)?",
            "key_points": [
                "Each attribute value is atomic for the chosen data model.",
                "There are no repeating groups or lists stored as multiple values in one cell.",
                "Rows can be distinguished by a key.",
            ],
            "retry_question": "If one cell stores several phone numbers as a comma-separated list, what 1NF issue does that raise?",
            "difficulty": "beginner",
            "topic": "normalization",
        },
        {
            "id": "dbms_norm_003",
            "question": "What is a partial functional dependency, and how does Second Normal Form address it?",
            "key_points": [
                "A partial dependency occurs when a non-key attribute depends on only part of a composite candidate key.",
                "A relation in 2NF is in 1NF.",
                "Every non-prime attribute is fully functionally dependent on each candidate key; no partial dependency remains.",
                "The partial-key-dependent attributes are separated into an appropriate relation during decomposition.",
            ],
            "retry_question": "For a key made of StudentID and CourseID, what would it mean if StudentName depended only on StudentID?",
            "difficulty": "intermediate",
            "topic": "normalization",
        },
        {
            "id": "dbms_norm_004",
            "question": "What is a transitive dependency, and what does Third Normal Form aim to remove?",
            "key_points": [
                "A transitive dependency occurs when a key determines a non-key attribute through another non-key attribute.",
                "3NF requires 2NF and no transitive dependency of non-prime attributes on a candidate key.",
                "A common formal definition allows X → A when X is a superkey or A is a prime attribute.",
            ],
            "retry_question": "If StudentID determines DepartmentID and DepartmentID determines DepartmentName, why might DepartmentName be separated?",
            "difficulty": "intermediate",
            "topic": "normalization",
        },
        {
            "id": "dbms_norm_005",
            "question": "What is Boyce-Codd Normal Form (BCNF), and how does it compare with 3NF?",
            "key_points": [
                "For every non-trivial functional dependency X → Y, BCNF requires X to be a superkey.",
                "BCNF is stricter than 3NF.",
                "A relation can satisfy 3NF but fail BCNF in cases involving overlapping candidate keys.",
            ],
            "retry_question": "In BCNF, what must the determinant X be for every non-trivial dependency X → Y?",
            "difficulty": "advanced",
            "topic": "normalization",
        },
        {
            "id": "dbms_norm_006",
            "question": "What are insertion, update, and deletion anomalies?",
            "key_points": [
                "An insertion anomaly makes it difficult to add one fact without adding an unrelated fact.",
                "An update anomaly means the same fact must be changed in multiple rows, risking inconsistency.",
                "A deletion anomaly means removing one fact can unintentionally remove another fact.",
            ],
            "retry_question": "If changing a department name requires editing many employee rows, which anomaly is that?",
            "difficulty": "beginner",
            "topic": "normalization",
        },
    ],
    "transactions": [
        {
            "id": "dbms_tx_001",
            "question": "Explain the ACID properties of a database transaction.",
            "key_points": [
                "Atomicity: the transaction completes as a unit or is rolled back.",
                "Consistency: a committed transaction preserves database constraints and invariants.",
                "Isolation: concurrent transactions are controlled so their effects meet the chosen isolation guarantees.",
                "Durability: committed changes survive failures according to the system's guarantees.",
            ],
            "retry_question": "Which ACID property means a committed payment should remain recorded after a restart?",
            "difficulty": "beginner",
            "topic": "transactions",
        },
        {
            "id": "dbms_tx_002",
            "question": "What is a transaction, and what do COMMIT and ROLLBACK do?",
            "key_points": [
                "A transaction is a logical unit of database work.",
                "COMMIT makes the transaction's changes final according to the DBMS guarantees.",
                "ROLLBACK undoes uncommitted changes in the transaction.",
            ],
            "retry_question": "Which command would you use to keep successful changes, and which to undo them?",
            "difficulty": "beginner",
            "topic": "transactions",
        },
        {
            "id": "dbms_tx_003",
            "question": "What is a deadlock in a database, and how can a DBMS respond to it?",
            "key_points": [
                "A deadlock occurs when transactions wait in a cycle for resources held by one another.",
                "The DBMS may detect the cycle and abort or roll back a victim transaction.",
                "Consistent resource ordering and short transactions can reduce deadlock risk.",
            ],
            "retry_question": "If transaction A waits for B's lock while B waits for A's lock, what has occurred?",
            "difficulty": "intermediate",
            "topic": "transactions",
        },
        {
            "id": "dbms_tx_004",
            "question": "What is the difference between optimistic and pessimistic concurrency control?",
            "key_points": [
                "Pessimistic control assumes conflicts may occur and uses locks or similar mechanisms early.",
                "Optimistic control allows work to proceed and checks for conflicts before commit or validation.",
                "The better approach depends on contention, workload, and implementation.",
            ],
            "retry_question": "Which approach lets transactions proceed first and checks for conflicts later?",
            "difficulty": "advanced",
            "topic": "transactions",
        },
    ],
    "indexes": [
        {
            "id": "dbms_idx_001",
            "question": "What is a database index, and what are its benefits and costs?",
            "key_points": [
                "An index is an auxiliary data structure that helps locate rows without scanning the whole table in suitable queries.",
                "It can improve reads, filtering, joins, and ordering when the query can use it.",
                "It consumes storage and adds work to inserts, updates, and deletes.",
                "The query planner and data distribution affect whether an index is used or beneficial.",
            ],
            "retry_question": "Why might adding an index speed up a lookup but slow down inserts?",
            "difficulty": "beginner",
            "topic": "indexes",
        },
        {
            "id": "dbms_idx_002",
            "question": "What is the difference between a clustered and a non-clustered index?",
            "key_points": [
                "A clustered index determines or closely corresponds to the row storage order in systems that support this concept.",
                "A non-clustered index is a separate structure that points to rows or row locations.",
                "Exact behavior and limits differ across database products; avoid assuming every DBMS uses the same terminology.",
            ],
            "retry_question": "Which type of index is typically described as controlling the physical or primary row order?",
            "difficulty": "intermediate",
            "topic": "indexes",
        },
        {
            "id": "dbms_idx_003",
            "question": "What is a composite index, and why does column order matter?",
            "key_points": [
                "A composite index contains more than one column.",
                "Many B-tree composite indexes are most directly useful for predicates that use the leading column or a leftmost prefix.",
                "Column order should reflect query patterns, selectivity, and sorting needs.",
            ],
            "retry_question": "For an index on (A, B), why may a query filtering only on B not benefit as much as one filtering on A?",
            "difficulty": "advanced",
            "topic": "indexes",
        },
    ],
}


def get_questions(topic=None):
    """Return questions for one topic, or a flattened list of all questions."""
    if topic is not None:
        return QUESTION_BANK.get(topic, [])
    return [question for questions in QUESTION_BANK.values() for question in questions]


if __name__ == "__main__":
    all_questions = get_questions()
    print(f"Loaded {len(all_questions)} interview questions across {len(QUESTION_BANK)} topics.")
    for topic, questions in QUESTION_BANK.items():
        print(f"- {topic}: {len(questions)}")
