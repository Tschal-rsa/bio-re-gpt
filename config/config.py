class Config:
    path = "BB"

    @property
    def dataset(self) -> str:
        if "DrugProt" in self.path:
            return "DrugProt"
        elif "DrugVar" in self.path:
            return "DrugVar"
        else:
            return self.path
    
    model = "gpt-4"