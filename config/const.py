from .struct import Entity, Relation, Sample, Result


class Const:
    data_path_template = "data/{}/dev.json"
    data_path_template_train = "data/{}/train.json"

    @classmethod
    def data_path(cls, dataset: str, is_train_set: bool) -> str:
        return cls.data_path_template_train.format(dataset) if is_train_set else cls.data_path_template.format(dataset)

    system_template = "You are stepping into the role of an expert assistant specialized in biomedicine. Your primary task is to accurately extract entities and relations from biomedical texts and respond to users' queries with clear, concise, and precise answers."
    system_template_ner = "You are stepping into the role of an expert assistant specialized in biomedicine. Your primary task is to accurately extract entities from biomedical texts and respond to users' queries with clear, concise, and precise answers."

    @classmethod
    def system_text(cls, ner: bool) -> str:
        return cls.system_template_ner if ner else cls.system_template

    question_template = "The entity types are {}, and the relation types are {}. {} What are the entities and the relation triplets of the text?"
    question_template_ner = "The entity types are {}. What are the entities of the text?"

    @classmethod
    def question_text(cls, dataset: str, ner: bool) -> str:
        if ner:
            return cls.question_template_ner.format(
                ", ".join(cls.task_ent_labels[dataset]),
            )
        else:
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
        'BC5CDR': ['Chemical', 'Disease'],
        'CRAFT': ['gene', 'allele', 'genome', 'polypeptide_domain', 'exon', 'QTL', 'primer', 'transcript', 'base_pair', 'transgene', 'sequence_variant', 'vector_replicon', 'promoter', 'plasmid', 'intron', 'gene_cassette', 'loxP_site', 'orthologous_region', 'single', 'double', 'pseudogene', 'flanked', 'targeting_vector', 'floxed', 'homologous', 'BAC', 'homologous_region', 'PCR_product', 'three_prime_UTR', 'SNP', 'EST', 'reverse', 'binding_site', 'forward', 'consensus', 'reverse_primer', 'forward_primer', 'stop_codon', 'start_codon', 'internal_ribosome_entry_site', 'siRNA', 'paralogous_region', 'antisense', 'haplotype', 'five_prime_UTR', 'nuclear_localization_signal', 'coiled_coil', 'origin_of_replication', 'assembly', 'inframe', 'H3K9_trimethylation_site', 'enhancer', 'insertion', 'exon_region', 'splice_site', 'insertion_site', 'FRT_site', 'cDNA_clone', 'rRNA_18S', 'circular', 'alternatively_spliced_transcript', 'ORF', 'propeptide', 'PAC', 'restriction_enzyme_binding_site', 'stop_gained', 'polyA_signal_sequence', 'polyA_sequence', 'regulatory_region', 'shRNA', 'polypeptide_catalytic_motif', 'gene_component_region', 'coding_exon', 'orthologous', 'five_prime_flanking_region', 'contig', 'TSS', 'genomic_clone', 'syntenic', 'plasmid_vector', 'restriction_fragment', 'paralogous', 'protein_coding', 'TF_binding_site', 'gap', 'exon_junction', 'syntenic_region', 'UTR', 'fragment_assembly', 'CDS_region', 'codon', 'orphan', 'AFLP_fragment', 'deletion_breakpoint', 'peptide_helix', 'reading_frame', 'predicted_gene', 'chromosome_breakpoint', 'three_prime_flanking_region', 'transmembrane_polypeptide_region', 'chromosome_arm', 'flanking_region', 'H3K9_dimethylation_site', 'mitochondrial_DNA', 'non_synonymous', 'inversion_site', 'five_prime_noncoding_exon', 'lysosomal_localization_signal', 'consensus_region', 'floxed_gene', 'pre_edited_mRNA', 'coding_region_of_exon', 'terminator', 'polyA_site', 'splice_junction', 'sterol_regulatory_element', 'intron_domain', 'nuclear_gene', 'genetic_marker', 'endosomal_localization_signal', 'simple_sequence_length_variation', 'gene_member_region', 'transcript_region', 'linkage_group', 'processed_pseudogene', 'UTR_region', 'alpha_helix', 'gene_fragment', 'mt_gene', 'STS', 'primer_binding_site', 'repeat_region', 'silencer', 'CDS_fragment', 'ds_oligo', 'proximal_promoter_element', 'predicted_transcript', 'T_to_G_transversion', 'insertion_breakpoint', 'cryptic', 'coding_start', 'match', 'linear', 'RFLP_fragment', 'dicistronic', 'protein_binding_site', 'stem_loop', 'primary_transcript', 'five_prime_coding_exon', 'dicistronic_transcript', 'fingerprint_map', 'DNA_binding_site', 'noncoding_exon', 'mating_type_region', 'expressed_sequence_assembly', 'rRNA_28S', 'open_chromatin_region', 'read', 'DNA_chromosome', 'polyadenylated_mRNA', 'CAAT_signal', 'cosmid', 'nuclear_export_signal', 'catalytic_residue', 'chimeric_cDNA_clone', 'recombination_signal_sequence', 'intergenic_region', 'transmembrane_helix', 'BAC_end', 'transcription_regulatory_region', 'polypeptide_binding_motif', 'morpholino_backbone', 'sequence_feature', 'synthetic_sequence', 'five_prime_intron', 'D_loop', 'transcription_end_site', 'lambda_vector', 'transcript_fusion', 'G_box', 'deletion_junction', 'intramembrane_polypeptide_region', 'transposable_element', 'antisense_RNA', 'dicistronic_mRNA', 'cap', 'mini_gene', 'overlapping_feature_set', 'transversion', 'cloned_cDNA_insert', 'FRT_flanked', 'mobile_genetic_element', 'five_prime_coding_exon_noncoding_region', 'branch_site', 'polypyrimidine_tract', 'bidirectional_promoter', 'T7_RNA_Polymerase_Promoter', 'three_prime_coding_exon_noncoding_region'],
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
        'BC5CDR': [
            'chemical-induced disease',
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
        'BC5CDR': {
            'chemical-induced disease': 'induces',
        },
    }

    task_limit_prompts = {
        "DrugProt": "In DrugProt, subjects must be CHEMICAL whereas objects must be GENE.",
        "DrugVar": "In DrugVar, subjects must be variant whereas objects must be drug.",
        "BC5CDR": "In BC5CDR, subjects must be Chemical whereas objects must be Disease.",
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
        "BC5CDR": [
            Sample(
                "The hypotensive effect of 100 mg/kg alpha-methyldopa was also partially reversed by naloxone.",
                Result(
                    {
                        Entity("naloxone", "Chemical"),
                        Entity("hypotensive", "Disease"),
                        Entity("alpha-methyldopa", "Chemical"),
                    },
                    {
                        Relation(
                            Entity("alpha-methyldopa", "Chemical"),
                            Entity("hypotensive", "Disease"),
                            "chemical-induced disease",
                        ),
                    },
                ),
            ),
            Sample(
                "Lidocaine-induced cardiac asystole.",
                Result(
                    {
                        Entity("cardiac asystole", "Disease"),
                        Entity("Lidocaine", "Chemical"),
                    },
                    {
                        Relation(
                            Entity("Lidocaine", "Chemical"),
                            Entity("cardiac asystole", "Disease"),
                            "chemical-induced disease",
                        ),
                    },
                ),
            ),
            Sample(
                "Suxamethonium infusion rate and observed fasciculations.",
                Result(
                    {
                        Entity("fasciculations", "Disease"),
                        Entity("Suxamethonium", "Chemical"),
                    },
                    {
                        Relation(
                            Entity("Suxamethonium", "Chemical"),
                            Entity("fasciculations", "Disease"),
                            "chemical-induced disease",
                        ),
                    },
                ),
            ),
            Sample(
                "Galanthamine hydrobromide, an anticholinesterase drug capable of penetrating the blood-brain barrier, was used in a patient demonstrating central effects of scopolamine (hyoscine) overdosage.",
                Result(
                    {
                        Entity("scopolamine", "Chemical"),
                        Entity("overdosage", "Disease"),
                        Entity("hyoscine", "Chemical"),
                        Entity("Galanthamine hydrobromide", "Chemical"),
                    },
                    {
                        Relation(
                            Entity("scopolamine", "Chemical"),
                            Entity("overdosage", "Disease"),
                            "chemical-induced disease",
                        ),
                        Relation(
                            Entity("hyoscine", "Chemical"),
                            Entity("overdosage", "Disease"),
                            "chemical-induced disease",
                        ),
                    },
                ),
            ),
            Sample(
                "Effects of uninephrectomy and high protein feeding on lithium-induced chronic renal failure in rats.",
                Result(
                    {
                        Entity("chronic renal failure", "Disease"),
                        Entity("lithium", "Chemical"),
                    },
                    {
                        Relation(
                            Entity("lithium", "Chemical"),
                            Entity("chronic renal failure", "Disease"),
                            "chemical-induced disease",
                        ),
                    },
                ),
            ),
        ],
        "CRAFT": [
            Sample(
                "Intraocular pressure in genetically distinct mice: an update and strain survey",
                Result(
                    {
                        Entity("genetically", "gene"),
                    },
                    set(),
                ),
            ),
            Sample(
                "Homozygosity for a null allele of the carbonic anhydrase II gene (Car2n) does not alter IOP while homozygosity for a mutation in the leptin receptor gene (Leprdb) that causes obesity and diabetes results in increased IOP.",
                Result(
                    {
                        Entity("gene", "gene"),
                        Entity("allele", "allele"),
                    },
                    set(),
                ),
            ),
            Sample(
                "Due to conservation in mammalian physiology and the powerful tools of mouse genetics, mice are a very important experimental system for probing the functions (both in health and disease) of many genes recently identified by sequencing the human genome [12].",
                Result(
                    {
                        Entity("genome", "genome"),
                        Entity("genes", "gene"),
                    },
                    set(),
                ),
            ),
            Sample(
                "Mcoln1 is highly similar to MCOLN1, especially in the transmembrane domains and ion pore region.",
                Result(
                    {
                        Entity("domains", "polypeptide_domain"),
                    },
                    set(),
                ),
            ),
            Sample(
                "The insertion allele also had a previously reported substitution (A to G, Thr164Ala) in exon 1 and several other single base changes in the promoter region [22].",
                Result(
                    {
                        Entity("allele", "allele"),
                        Entity("exon", "exon"),
                        Entity("promoter", "promoter"),
                    },
                    set(),
                ),
            ),
        ],
    }
