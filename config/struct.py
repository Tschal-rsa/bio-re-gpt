from dataclasses import dataclass, field
from typing import Self
import re


class BundleConst:
    left_border = "<"
    right_border = ">"
    separator = "|"
    bundle_pattern = re.compile(f"{left_border}.+?{right_border}")


@dataclass(frozen=True)
class Entity:
    name: str
    etype: str

    def __str__(self) -> str:
        return (
            BundleConst.left_border
            + BundleConst.separator.join([self.name, self.etype])
            + BundleConst.right_border
        )


@dataclass(frozen=True)
class Relation:
    subject: Entity
    object: Entity
    rtype: str

    def __str__(self) -> str:
        return (
            BundleConst.left_border
            + BundleConst.separator.join(
                [
                    self.subject.name,
                    self.subject.etype,
                    self.object.name,
                    self.object.etype,
                    self.rtype,
                ]
            )
            + BundleConst.right_border
        )


@dataclass
class Result:
    entities: set[Entity] = field(default_factory=set)
    relations: set[Relation] = field(default_factory=set)


@dataclass
class Sample:
    text: str
    result: Result


@dataclass
class EvalBundle:
    tp: int = 0
    fp: int = 0
    fn: int = 0

    def __iadd__(self, other: Self) -> Self:
        self.tp += other.tp
        self.fp += other.fp
        self.fn += other.fn
        return self

    def __str__(self) -> str:
        precision = self.tp / (self.tp + self.fp) if (self.tp + self.fp) > 0 else 0.0
        recall = self.tp / (self.tp + self.fn) if (self.tp + self.fn) > 0 else 0.0
        f1 = (
            2 * self.tp / (2 * self.tp + self.fp + self.fn)
            if (2 * self.tp + self.fp + self.fn) > 0
            else 0.0
        )
        return (
            f"P:\t{100 * precision:.2f}%\nR:\t{100 * recall:.2f}%\nF1:\t{100 * f1:.2f}%"
        )


@dataclass
class Eval:
    entity: EvalBundle = field(default_factory=EvalBundle)
    relation: EvalBundle = field(default_factory=EvalBundle)

    def __iadd__(self, other: Self) -> Self:
        self.entity += other.entity
        self.relation += other.relation
        return self

    def __str__(self) -> str:
        return "\n".join(
            [
                " NER ".center(14, "="),
                str(self.entity),
                " RE ".center(14, "="),
                str(self.relation),
            ]
        )


def decompass(bundle: str) -> Entity | Relation | None:
    tup = bundle[len(BundleConst.left_border) : -len(BundleConst.right_border)].split(
        BundleConst.separator
    )
    if len(tup) == 2:
        return Entity(tup[0], tup[1])
    elif len(tup) == 5:
        return Relation(Entity(tup[0], tup[1]), Entity(tup[2], tup[3]), tup[4])
    else:
        return None


def extract(response: str) -> Result:
    result = Result()
    for bundle in BundleConst.bundle_pattern.findall(response):
        struct = decompass(bundle)
        if isinstance(struct, Entity):
            result.entities.add(struct)
        elif isinstance(struct, Relation):
            result.relations.add(struct)
        # else ignore None
    return result


def evaluate(response: str, veritas: Result) -> Eval:
    prediction = extract(response)
    return Eval(
        EvalBundle(
            len(prediction.entities & veritas.entities),
            len(prediction.entities - veritas.entities),
            len(veritas.entities - prediction.entities),
        ),
        EvalBundle(
            len(prediction.relations & veritas.relations),
            len(prediction.relations - veritas.relations),
            len(veritas.relations - prediction.relations),
        ),
    )
