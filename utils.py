
import emoji

# # https://stackoverflow.com/questions/33404752/removing-emojis-from-a-string-in-python/50602709#50602709
def clean_text(text):
    try: return  emoji.replace_emoji(text.decode('utf8'), replace='')
    except AttributeError: return  emoji.replace_emoji(text, replace='')
     



# if __name__ == '__main__':
#     text = 'For you'
    
#     t = clean_text(" ".join(text.split()))
#     print(t)

#     if not t:
#         print(1)


