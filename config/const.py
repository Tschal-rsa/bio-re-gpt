from .struct import Entity, Relation, Sample, Result


class Const:
    data_path_template = "data/{}/dev.json"

    @classmethod
    def data_path(cls, dataset: str) -> str:
        return cls.data_path_template.format(dataset)

    system_text = "You are stepping into the role of an expert assistant specialized in biomedicine. Your primary task is to accurately extract entities and relations from biomedical texts and respond to users' queries with clear, concise, and precise answers."

    question_template = "The entity types are {}, and the relation types are {}. {} What are the entities and the relation triplets of the text?"

    @classmethod
    def question_text(cls, dataset: str) -> str:
        return cls.question_template.format(
            ", ".join(cls.task_ent_labels[dataset]),
            ", ".join(cls.task_rel_labels[dataset]),
            cls.task_limit_prompts[dataset],
        )

    answer_entity_template = "Because {} is a {}, {} is a valid entity."
    answer_relation_template = "Because {} {} {}, {} is a valid relation triplet."

    @classmethod
    def answer_text(cls, dataset, result: Result) -> str:
        return " ".join(
            [
                cls.answer_entity_template.format(
                    entity.name, entity.etype, str(entity)
                )
                for entity in result.entities
            ]
            + [
                cls.answer_relation_template.format(
                    relation.subject.name,
                    cls.task_umls_rels[dataset][relation.rtype],
                    relation.object.name,
                    str(relation),
                )
                for relation in result.relations
            ]
        )

    task_ent_labels = {
        "DrugProt": ["CHEMICAL", "GENE"],
        "DrugVar": ["drug", "variant"],
    }

    task_rel_labels = {
        "DrugProt": [
            "product or substrate",
            "activator",
            "agonist or antagonist",
            "regulator",
            "part of",
            "inhibitor",
        ],
        "DrugVar": [
            "resistance",
            "resistance or non-response",
            "response",
            "sensitivity",
        ],
    }

    task_umls_rels = {
        "DrugProt": {
            "product or substrate": "acts as a product or substrate to",
            "activator": "acts as an activator to",
            "agonist or antagonist": "acts as an agonist or antagonist to",
            "regulator": "acts as a regulator to",
            "part of": "acts as a part to",
            "inhibitor": "acts as an inhibitor to",
        },
        "DrugVar": {
            "resistance": "acts as the resistance to",
            "resistance or non-response": "does not response to",
            "response": "responses to",
            "sensitivity": "is sensitive to",
        },
    }

    task_limit_prompts = {
        "DrugProt": "In DrugProt, subjects must be CHEMICAL whereas objects must be GENE.",
        "DrugVar": "In DrugVar, subjects must be variant whereas objects must be drug.",
    }

    task_examples = {
        "DrugProt": [
            Sample(
                "The P-gp- and BCRP-facilitated transport of apixaban was concentration- and time-dependent and did not show saturation over a wide range of concentrations (1-100 μM). The efflux transport of apixaban was also demonstrated by the lower mucosal-to-serosal permeability than that of the serosal-to-mucosal direction in isolated rat jejunum segments.",
                Result(
                    {
                        Entity("apixaban", "CHEMICAL"),
                        Entity("P-gp", "GENE"),
                        Entity("BCRP", "GENE"),
                    },
                    {
                        Relation(
                            Entity("apixaban", "CHEMICAL"),
                            Entity("P-gp", "GENE"),
                            "product or substrate",
                        ),
                        Relation(
                            Entity("apixaban", "CHEMICAL"),
                            Entity("BCRP", "GENE"),
                            "product or substrate",
                        ),
                    },
                ),
            ),
            Sample(
                "Menthol, popularly known for its cooling effect, activates TRPM8--a cold-activated thermoTRP ion channel.",
                Result(
                    {
                        Entity("Menthol", "CHEMICAL"),
                        Entity("TRPM8", "GENE"),
                        Entity("thermoTRP ion channel", "GENE"),
                    },
                    {
                        Relation(
                            Entity("Menthol", "CHEMICAL"),
                            Entity("TRPM8", "GENE"),
                            "activator",
                        ),
                        Relation(
                            Entity("Menthol", "CHEMICAL"),
                            Entity("thermoTRP ion channel", "GENE"),
                            "activator",
                        ),
                    },
                ),
            ),
            Sample(
                "Our studies demonstrated that (a) stereoselective and rank order differences exist among the direct effects of ephedrine isomers; (b) 1R,2S-ephedrine is the most potent of the four ephedrine isomers on all three human beta-AR; and (c) 1R,2S- ephedrine was nearly equipotent as a beta1-/beta2-AR agonist and the only isomer possessing weak partial agonist activity on beta3-AR.",
                Result(
                    {
                        Entity("ephedrine", "CHEMICAL"),
                        Entity("1R,2S-ephedrine", "CHEMICAL"),
                        Entity("1R,2S- ephedrine", "CHEMICAL"),
                        Entity("human beta-AR", "GENE"),
                        Entity("beta1-/beta2-AR", "GENE"),
                        Entity("beta3-AR", "GENE"),
                    },
                    {
                        Relation(
                            Entity("ephedrine", "CHEMICAL"),
                            Entity("human beta-AR", "GENE"),
                            "agonist or antagonist",
                        ),
                        Relation(
                            Entity("1R,2S-ephedrine", "CHEMICAL"),
                            Entity("human beta-AR", "GENE"),
                            "agonist or antagonist",
                        ),
                        Relation(
                            Entity("1R,2S-ephedrine", "CHEMICAL"),
                            Entity("beta3-AR", "GENE"),
                            "agonist or antagonist",
                        ),
                    },
                ),
            ),
            Sample(
                "When delta-receptor binding was determined by using [3H]DPDPE, a 40-50% decrease in binding in the midbrain and cortex, and 25-35% decrease in binding in the striatum were observed after 3 or 4 days of DPDPE treatment.",
                Result(
                    {
                        Entity("DPDPE", "CHEMICAL"),
                        Entity("[3H]DPDPE", "CHEMICAL"),
                        Entity("delta-receptor", "GENE"),
                    },
                    {
                        Relation(
                            Entity("[3H]DPDPE", "CHEMICAL"),
                            Entity("delta-receptor", "GENE"),
                            "regulator",
                        ),
                        Relation(
                            Entity("DPDPE", "CHEMICAL"),
                            Entity("delta-receptor", "GENE"),
                            "regulator",
                        ),
                    },
                ),
            ),
            Sample(
                "The in vitro covalent binding was inhibited in the presence of beta-aminopropionitrile, D-penicillamine, and hydralazine, which suggested that the aldehyde group of allysine in human elastin was relevant to the covalent binding.",
                Result(
                    {
                        Entity("beta-aminopropionitrile", "CHEMICAL"),
                        Entity("D-penicillamine", "CHEMICAL"),
                        Entity("hydralazine", "CHEMICAL"),
                        Entity("aldehyde", "CHEMICAL"),
                        Entity("allysine", "CHEMICAL"),
                        Entity("human elastin", "GENE"),
                    },
                    {
                        Relation(
                            Entity("beta-aminopropionitrile", "CHEMICAL"),
                            Entity("human elastin", "GENE"),
                            "inhibitor",
                        ),
                        Relation(
                            Entity("aldehyde", "CHEMICAL"),
                            Entity("human elastin", "GENE"),
                            "part of",
                        ),
                        Relation(
                            Entity("allysine", "CHEMICAL"),
                            Entity("human elastin", "GENE"),
                            "part of",
                        ),
                        Relation(
                            Entity("D-penicillamine", "CHEMICAL"),
                            Entity("human elastin", "GENE"),
                            "inhibitor",
                        ),
                        Relation(
                            Entity("hydralazine", "CHEMICAL"),
                            Entity("human elastin", "GENE"),
                            "inhibitor",
                        ),
                    },
                ),
            ),
        ],
        "DrugVar": [
            Sample(
                "Studies of ALK rearranged lung cancers with acquired resistance to crizotinib have identified ALK fusion gene amplification and secondary ALK TK domain mutations ( L1196M and G1269A ) in about one third of cases .",
                Result(
                    {
                        Entity("crizotinib", "drug"),
                        Entity("L1196M", "variant"),
                        Entity("G1269A", "variant"),
                    },
                    {
                        Relation(
                            Entity("L1196M", "variant"),
                            Entity("crizotinib", "drug"),
                            "resistance",
                        ),
                        Relation(
                            Entity("G1269A", "variant"),
                            Entity("crizotinib", "drug"),
                            "resistance",
                        ),
                    },
                ),
            ),
            Sample(
                "Importantly , the wild type protein formed fibrils only at 10 μM erlotinib , whereas the TKI-sensitive mutants relocated to fibrils in the presence of 10–100 nM erlotinib , and this effect was fully abrogated by the erlotinib-resistant T790M mutation .",
                Result(
                    {
                        Entity("μM erlotinib", "drug"),
                        Entity("erlotinib-resistant T790M", "variant"),
                        Entity("nM erlotinib", "drug"),
                        Entity("the erlotinib-resistant", "drug"),
                    },
                    {
                        Relation(
                            Entity("erlotinib-resistant T790M", "variant"),
                            Entity("μM erlotinib", "drug"),
                            "resistance or non-response",
                        ),
                        Relation(
                            Entity("erlotinib-resistant T790M", "variant"),
                            Entity("nM erlotinib", "drug"),
                            "resistance or non-response",
                        ),
                        Relation(
                            Entity("erlotinib-resistant T790M", "variant"),
                            Entity("the erlotinib-resistant", "drug"),
                            "resistance or non-response",
                        ),
                    },
                ),
            ),
            Sample(
                "Second generation EGFR TKIs e.g. , BIBW 2992 ( afatinib ) and PF00299804 ( dacomitinib ) , and third generation EGFR TKIs e.g. , CO-1686 and AZD9291 are irreversible inhibitors that could overcome the AR caused by T790M .",
                Result(
                    {
                        Entity("BIBW 2992", "drug"),
                        Entity("T790M", "variant"),
                        Entity("afatinib", "drug"),
                    },
                    {
                        Relation(
                            Entity("T790M", "variant"),
                            Entity("BIBW 2992", "drug"),
                            "response",
                        ),
                        Relation(
                            Entity("T790M", "variant"),
                            Entity("afatinib", "drug"),
                            "response",
                        ),
                    },
                ),
            ),
            Sample(
                "( D ) COS-7 cells with stable transduced expression of L858R or L858R+E884K mutant EGFR were tested in cellular cytotoxicity assay in vitro under drug treatment with either erlotinib or gefitinib at indicated concentrations .",
                Result(
                    {
                        Entity("gefitinib", "drug"),
                        Entity("L858R", "variant"),
                        Entity("erlotinib", "drug"),
                    },
                    {
                        Relation(
                            Entity("L858R", "variant"),
                            Entity("gefitinib", "drug"),
                            "response",
                        ),
                        Relation(
                            Entity("L858R", "variant"),
                            Entity("erlotinib", "drug"),
                            "response",
                        ),
                    },
                ),
            ),
        ],
    }
