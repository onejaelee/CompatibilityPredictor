# CompatibilityPredictor
Takes in a json file within the same folder as the **compatibilityPredictor.py** named **input.json** and outputs a weighted cosine similarity score based on the average team attribute values cosine similarity score to a specific candidate. 

Intelligence is weighted the highest and spicyFoodTolerance is weighted the lowest. However, it can generally work with any amount of attributes as long as the team and candidate has the same amount of attributes. This works for any range of attribute value that is non-negative and outputs a score between **0 to 1**. This score is essentially seeing how the ratio of attribute values for a candidate matches with the overall team to see how well the personality matches, rather than the magnitude of the attributes individually.
