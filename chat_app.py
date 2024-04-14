from openai import OpenAI
import streamlit as st

st.title("Pizza order Bot!")


client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
MODEL = st.secrets["OPENAI_MODEL"]



pizza_menu = """
    pepperoni pizza  12.95, 10.00, 7.00 \
    cheese pizza   10.95, 9.25, 6.50 \
    eggplant pizza   11.95, 9.75, 6.75 \
    fries 4.50, 3.50 \
    greek salad 7.25 \
    Toppings: \
    extra cheese 2.00, \
    mushrooms 1.50 \
    sausage 3.00 \
    canadian bacon 3.50 \
    AI sauce 1.50 \
    peppers 1.00 \
    Drinks: \
    coke 3.00, 2.00, 1.00 \
    sprite 3.00, 2.00, 1.00 \
    bottled water 5.00 \
"""
MESSAGES = [ {'role':'system', 'content':f"""You are OrderBot, an automated service to collect orders for a pizza restaurant. \
    You first greet the customer, then collects the order, \
    and then asks if it is a pickup or delivery. \
    You wait to collect the entire order, then summarize it and check for a final \
    time if the customer wants to add anything else. \
    If it is a delivery, you ask for an address. \
    Finally you collect the payment.\
    Make sure to clarify all options, extras and sizes to uniquely \
    identify the item from the menu.\
    You respond in a short, very conversational friendly style. \
    The menu includes \
    {pizza_menu}
"""} ]



def conversation(temperature=0.2, token=1000, stream=True):
    print(st.session_state.messages)
    completion = client.chat.completions.create(
        model=MODEL,
        messages=MESSAGES + st.session_state.messages,
        temperature=temperature,
        stop=None,
        n=1,
        max_tokens=token,
        stream=stream
    )
    return completion


if "messages" not in st.session_state:
    st.session_state.messages = []
    resp = conversation(stream=False)
    resp = resp.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": resp})



for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("What would you like to order!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        resp = st.write_stream(conversation())
    st.session_state.messages.append({"role": "assistant", "content": resp})
