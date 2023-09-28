from config import Entity, Relation, Sample, Result, Const, Config
import json


class UniDataset:
    def __init__(self, config: Config) -> None:
        path = Const.data_path(config.path)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.samples: list[Sample] = []
        for example in data:
            text = example["text"]
            entity_dict: dict[str, str] = {}
            result = Result()
            for entity in example["entity_list"]:
                entity_name = entity["name"]
                entity_type = entity["ent_type"]
                entity_dict[entity_name] = entity_type
                result.entities.add(Entity(entity_name, entity_type))
            for relation in example["relation_list"]:
                subject_name = relation["subject"]
                object_name = relation["object"]
                subject = Entity(subject_name, entity_dict[subject_name])
                object = Entity(object_name, entity_dict[object_name])
                result.relations.add(Relation(subject, object, relation["rel_type"]))
            self.samples.append(Sample(text, result))

    def __getitem__(self, index: int) -> Sample:
        return self.samples[index]

    def __len__(self) -> int:
        return len(self.samples)
