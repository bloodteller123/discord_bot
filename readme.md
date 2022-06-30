## Discord Chatting bot prototype
Training/Evaluation codes mostly come from this [Turotials](https://towardsdatascience.com/make-your-own-rick-sanchez-bot-with-transformers-and-dialogpt-fine-tuning-f85e6d1f4e30) <br/>
The original model comes from [microsoft/DialoGPT-medium](https://huggingface.co/microsoft/DialoGPT-medium) and is finetuned on a [discord-conversation-dataset](https://www.reddit.com/r/datasets/comments/la6zuq/massive_multiturn_conversational_dataset_based_on/
) <br/><br/>

The dataset is not pre-processed as it's just a large chunks of conversation dialogue in a text file. Regex is mainly used to extract the useful data from the file. <br/><br/>

### TODO
1. Limit the frequency of sending requests to discord
2. IDK <br/>

### Prerequisites
```python
pip install torch
pip install transformers
pip install discord
```
