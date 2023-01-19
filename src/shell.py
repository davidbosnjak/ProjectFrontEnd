import language
import os
import openai
import sys

text = prompt = sys.argv[1]
result, error = language.run('<stdin>', text)

if error: print(error.as_string())
elif result: print(result)