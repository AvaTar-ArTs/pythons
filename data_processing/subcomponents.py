import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
"""
A benchmark which tries to compare the possible slow subparts of validation.
"""

from jsonschema import Draft202012Validator
from referencing import Registry
from referencing.jsonschema import DRAFT202012
from rpds import HashTrieMap, HashTrieSet

schema = {
    "type": "array",
    "minLength": 1,
    "maxLength": 1,
    "items": {"type": "integer"},
}

hmap = HashTrieMap()
hset = HashTrieSet()

registry = Registry()

v = Draft202012Validator(schema)


def registry_data_structures():
    """registry_data_structures function."""

    return hmap.insert("foo", "bar"), hset.insert("foo")

    """registry_add function."""


def registry_add():
    resource = DRAFT202012.create_resource(schema)
    return registry.with_resource(uri="urn:example", resource=resource)


try:
        from pyperf import Runner
        runner = Runner()
        runner.bench_func("HashMap/HashSet insertion", registry_data_structures)
        runner.bench_func("Registry insertion", registry_add)
        runner.bench_func("Success", lambda: v.is_valid([1]))
        runner.bench_func("Failure", lambda: v.is_valid(["foo"]))
        runner.bench_func("Metaschema validation", lambda: v.check_schema(schema))
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)