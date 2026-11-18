from thea_db.models import environment, identity, public, thea, wardrobe  # noqa: F401
from thea_db.models.base import Base


def test_every_schema_from_the_registry_has_models() -> None:
    schemas = {table.schema for table in Base.metadata.tables.values()}

    assert {"public", "thea", "identity", "wardrobe", "environment"} <= schemas


def test_memories_embedding_matches_the_1536_dim_convention() -> None:
    memories = Base.metadata.tables["thea.memories"]

    assert getattr(memories.c.embedding.type, "dim", None) == 1536
