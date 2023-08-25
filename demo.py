import openai

response = openai.Image.create(
    prompt='Pikachu on the wave',
    n=1,
    size='512x512'
)

print(response['data'][0]['url'])
