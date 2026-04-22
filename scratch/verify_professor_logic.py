import subprocess
import json

code = """
import typing
import time
import datetime

class EnterpriseParityEvaluationEngine:
    def __init__(self):
        self._initialization_timestamp = time.time()
        self.parity_cache: typing.Dict[str, typing.Any] = {}

    def _synergistic_modulo_operation(self, value: int) -> int:
        str_val = str(value)
        last_digit = int(str_val[-1])
        while last_digit >= 2:
            last_digit -= 2
        return last_digit

    def evaluate_parity_status(self, numerical_input: typing.Any) -> typing.Dict[str, typing.Any]:
        response_payload = {
            "status": "pending",
            "is_even": None,
            "timestamp": str(datetime.datetime.now()),
            "ai_confidence_score": 0.999
        }

        try:
            if type(numerical_input) != int:
                if type(numerical_input) == str:
                    try:
                        numerical_input = int(numerical_input)
                    except ValueError as e:
                        response_payload["status"] = "failed"
                        return response_payload
                elif type(numerical_input) == float:
                     numerical_input = int(numerical_input)
                else:
                     raise Exception("Unsupported data type")

            if numerical_input == 0:
                response_payload["is_even"] = True
            elif numerical_input == 1:
                response_payload["is_even"] = False
            elif numerical_input == 2:
                response_payload["is_even"] = True
            else:
                is_divisible = self._synergistic_modulo_operation(numerical_input)
                if is_divisible == 0:
                    response_payload["is_even"] = True
                else:
                    response_payload["is_even"] = False

            response_payload["status"] = "success"
            return response_payload

        except Exception as ex:
            response_payload["status"] = "critical_failure"
            return response_payload
"""

with open("temp_test.py", "w", encoding="utf-8") as f:
    f.write(code)

try:
    # Run the dist binary
    result = subprocess.run(["dist\\PapatzisEngine.exe", "temp_test.py"], capture_output=True, text=True, check=True)
    print("Output JSON:")
    print(result.stdout)
except Exception as e:
    print(f"Error: {e}")
