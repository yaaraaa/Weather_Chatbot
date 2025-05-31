import json
from llama_cloud_services import LlamaExtract
from llama_cloud.core.api_error import ApiError


class DataExtractor:
    """Extracts structured data from PDFs using a LlamaExtract agent."""

    def __init__(self, agent_name, input_pdf_path, output_json_path):
        """Initialize extractor with agent name, PDF path, and output file path."""

        self.agent_name = agent_name
        self.input_pdf_path = input_pdf_path
        self.output_json_path = output_json_path
        self.extractor = LlamaExtract()
        self.schema = self._get_schema()
        self.agent = self._initialize_agent()

    def _get_schema(self):
        """Define the data schema for extraction."""

        return {
            "description": "Structured data for outdoor activities and clothing suggestions by weather and country.",
            "type": "object",
            "required": ["weather_types"],
            "properties": {
                "weather_types": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["weather", "countries"],
                        "properties": {
                            "weather": {
                                "type": "string",
                                "description": "Type of weather (e.g., Sunny, Rainy, Snowy, Windy, Cloudy)",
                            },
                            "countries": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "required": [
                                        "country",
                                        "outdoor_activities",
                                        "appropriate_clothing",
                                    ],
                                    "properties": {
                                        "country": {
                                            "type": "string",
                                            "description": "Name of the country",
                                        },
                                        "outdoor_activities": {
                                            "type": "string",
                                            "description": "Outdoor activity appropriate for this weather in this country",
                                        },
                                        "appropriate_clothing": {
                                            "type": "string",
                                            "description": "Clothing recommendation suitable for the weather in this country",
                                        },
                                    },
                                },
                            },
                        },
                    },
                }
            },
        }

    def _initialize_agent(self):
        """Fetch or create a LlamaExtract agent based on schema."""

        try:
            return self.extractor.get_agent(self.agent_name)
        except ApiError as e:
            if e.status_code == 404:
                print(f"Agent '{self.agent_name}' not found. Creating a new one...")
                return self.extractor.create_agent(
                    name=self.agent_name, data_schema=self.schema
                )
            raise RuntimeError(f"API error while retrieving agent: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error: {e}")

    def extract_and_save(self):
        """Run extraction on the input PDF and save output to JSON."""

        print(f"Extracting data from PDF: {self.input_pdf_path}")
        result = self.agent.extract(self.input_pdf_path)
        data = result.data

        print(f"Saving extracted data to: {self.output_json_path}")
        with open(self.output_json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("Data extraction and saving completed successfully.")
