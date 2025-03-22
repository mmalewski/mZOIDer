import json

class Meta:
    def __init__(self, PivotLocation, PivotRotation, PrintedMeshExtent, Title, Description) -> None:
        """Initializes the meta data."""
        self.PivotLocation = PivotLocation
        self.PivotRotation = PivotRotation
        self.PrintedMeshExtent = PrintedMeshExtent
        self.Title = Title
        self.Description = Description
        
        
    def to_json(self) -> str:
        """Converts the meta data to a JSON string."""
        
        meta_dict = {
            "PivotLocation": self.PivotLocation,
            "PivotRotation": self.PivotRotation,
            "PrintedMeshExtent": self.PrintedMeshExtent,
            "Title": self.Title,
            "Description": self.Description
        }
        
        return json.dumps(meta_dict, indent=4)
    
    
    def export_to_file(self, filename) -> bool:
        """Exports the meta data to a file."""
        json_data = self.to_json()
        
        with open(filename, 'w+') as file:
            file.write(json_data)
            file.close()
            
        return True