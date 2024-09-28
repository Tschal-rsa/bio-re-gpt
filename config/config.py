class Config:
    path = "DrugVar"

    @property
    def dataset(self) -> str:
        if "DrugProt" in self.path:
            return "DrugProt"
        elif "DrugVar" in self.path:
            return "DrugVar"
        else:
            return self.path
    
    @property
    def ner(self) -> bool:
        return "CRAFT" in self.dataset
    
    is_train_set = False

    model = "gpt-4"