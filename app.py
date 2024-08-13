import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from duckduckgo_search import DDGS
import requests
import base64
import time
import concurrent.futures


# Load environment variables
load_dotenv()
LLAMA_API = os.getenv("LLAMA_API")
OCR_API = os.getenv("OCR_API")

# Initialize the Groq client
client = Groq(api_key=LLAMA_API)



def temporary_text(text, duration=2):
    placeholder = st.empty()
    placeholder.warning(text)
    time.sleep(duration)
    placeholder.empty()

def extract_text_from_image(image_path):
    try:
        url = "https://api.ocr.space/parse/image"
        payload = {
            "apikey": OCR_API,
            "language": "eng",
            "OCREngine": "2",
            "isOverlayRequired": False
        }
        with open(image_path, "rb") as image_file:
            files = {"file": image_file}
            response = requests.post(url, files=files, data=payload)
        response.raise_for_status()
        result = response.json()
        
        if not result.get("IsErroredOnProcessing"):
            extracted_text = " ".join([page["ParsedText"] for page in result["ParsedResults"]])
            return extracted_text.strip()
        else:
            print(f"Error processing image: {result.get('ErrorMessage', 'Unknown error')}")
            return None
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

def identify_medical_condition(text):
    prompt = f"Identify the medical condition or symptoms from the following text. Be specific and concise:\n\n{text}"
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a medical expert. Identify medical conditions or symptoms from the given text."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=100,
            top_p=1,
            stream=False
        )
        
        if completion.choices and len(completion.choices) > 0:
            return completion.choices[0].message.content.strip()
        else:
            return "No medical condition identified"
    except Exception as e:
        print(f"Error identifying medical condition: {e}")
        return "Error in identifying medical condition"

def get_remedy(condition, remedy_type):
    prompt = f"Provide a detailed {remedy_type} remedy for {condition}. Include specific ingredients or treatments."
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {"role": "system", "content": f"You are an expert in {remedy_type} remedies. Provide detailed and accurate information."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=200,
            top_p=1,
            stream=False
        )
        
        if completion.choices and len(completion.choices) > 0:
            return completion.choices[0].message.content.strip()
        else:
            return f"No {remedy_type} remedy found"
    except Exception as e:
        print(f"Error getting remedy: {e}")
        return f"Error in getting {remedy_type} remedy"

def get_remedy_images(query, num_images=3):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.images(query, max_results=num_images*2))  # Fetch more images to account for duplicates
        unique_images = list(set(result['image'] for result in results))
        return unique_images[:num_images]  # Return only the required number of unique images
    except Exception as e:
        print(f"Error fetching images for {query}: {e}")
        return []

def review_answer(condition, initial_answer):
    prompt = f"""As a medical review expert, critically evaluate the following diagnosis and remedy for accuracy and completeness:

Condition: {condition}
Initial Answer: {initial_answer}

Please provide your assessment in the following format:
1. Accuracy of diagnosis:
2. Completeness of remedies:
3. Any missing important information:
4. Suggested improvements or corrections:
5. Overall assessment (Correct/Partially Correct/Incorrect):

Be thorough in your evaluation."""

    try:
        full_review = ""
        while len(full_review.split()) < 500:  # Adjust this number as needed
            completion = client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a highly skilled medical review expert. Your task is to critically evaluate medical diagnoses and remedies for accuracy and completeness."},
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": full_review},
                    {"role": "user", "content": "Continue from where you left off:"}
                ],
                temperature=0.3,
                max_tokens=300,
                top_p=1,
                stream=False
            )
            
            if completion.choices and len(completion.choices) > 0:
                chunk = completion.choices[0].message.content.strip()
                full_review += " " + chunk
                if chunk.endswith(".") or chunk.endswith(":"):
                    break
            else:
                break

        return full_review.strip()
    except Exception as e:
        print(f"Error in reviewing answer: {e}")
        return "Error in reviewing the answer"



def process_user_request(query=None, image_path=None):
    try:
        if image_path:
            extracted_text = extract_text_from_image(image_path)
            if not extracted_text:
                return "Failed to extract text from document."
            condition = identify_medical_condition(extracted_text)
        elif query:
            condition = identify_medical_condition(query)
        else:
            return "No valid input provided."

        if not condition or condition.lower() == "no medical condition identified":
            return "Could not identify any medical condition."

        remedy_types = ["home", "Ayurvedic", "homeopathic", "allopathic"]
        remedies = {}
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_remedy = {executor.submit(get_remedy, condition, remedy_type): remedy_type for remedy_type in remedy_types}
            future_to_images = {executor.submit(get_remedy_images, f"{condition} {remedy_type} remedy"): remedy_type for remedy_type in remedy_types}
            
            for future in concurrent.futures.as_completed(future_to_remedy):
                remedy_type = future_to_remedy[future]
                remedies[f"{remedy_type}_remedy"] = {"description": future.result()}
            
            for future in concurrent.futures.as_completed(future_to_images):
                remedy_type = future_to_images[future]
                remedies[f"{remedy_type}_remedy"]["images"] = future.result()

        all_remedies = "\n\n".join([f"{key}:\n{value['description']}" for key, value in remedies.items()])
        review = review_answer(condition, all_remedies)

        return {"condition": condition, "remedies": remedies, "review": review}
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def remove_old_uploads():
    upload_dir = "uploads"
    if os.path.exists(upload_dir):
        for filename in os.listdir(upload_dir):
            file_path = os.path.join(upload_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return f"data:image/png;base64,{encoded_string}"

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    # Add Font Awesome CSS
    st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">', unsafe_allow_html=True)


def display_results(result):
    if isinstance(result, str):
        st.error(result)
    else:
        st.success(f"Identified Condition: {result['condition']}")
        
        # Add disclaimer
        temporary_text("DISCLAIMER: The information provided here is for educational purposes only and should not be considered medical advice. Always consult with a qualified healthcare professional before starting any treatment or taking any medication.")
        
        for remedy_type, info in result['remedies'].items():
            # Remove 'Remedy' from the key to avoid duplication
            remedy_title = remedy_type.replace('_remedy', '').capitalize()
            with st.expander(f"{remedy_title} Remedies", expanded=True):
                st.markdown(f"""
                    <div class="scrollable-content">
                        {info['description']}
                    </div>
                """, unsafe_allow_html=True)
                if info['images']:
                    st.write("Remedy Images:")
                    cols = st.columns(len(info['images']))
                    for i, url in enumerate(info['images']):
                        with cols[i]:
                            st.image(url, width=200)
                else:
                    st.info("No images found for this remedy.")

def add_footer():
    footer_html = """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(51, 51, 51, 0.8);
        color: white;
        text-align: center;
        padding: 10px 0;
        z-index: 1000;
    }
    .footer a {
        color: white;
        text-decoration: none;
        margin: 0 15px;
        font-size: 24px;
    }
    .footer a:hover {
        opacity: 0.8;
    }
    </style>
    <div class="footer">
        <a href="https://www.linkedin.com/in/sayan-maity-756b8b244/" target="_blank">
            <i class="fab fa-linkedin"></i>
        </a>
        <a href="https://github.com/Sayan-Maity-Code" target="_blank">
            <i class="fab fa-github"></i>
        </a>
        <a href="https://www.instagram.com/joy_in_knowledge/" target="_blank">
            <i class="fab fa-instagram"></i>
        </a>
        
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="FriendlyClinic: A Smart & Personalized Medical Assistant", layout="wide")
    
    local_css("style.css")
    
    bg_img = add_bg_from_local('background.jpg')
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{bg_img}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            height: 100vh;
            width: 100%;
        }}
        @media (max-width: 768px) {{
            .stApp {{
                background-size: contain;
                background-position: center;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("""
        <h1 class='title'>FriendlyClinic: AI Personalized Medical Assistant</h1>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3])

    with col1:
        input_type = st.radio("Select input type:", ["Text", "Image"])

    with col2:
        if input_type == "Text":
            user_input = st.text_area("Enter your symptoms or medical condition:")
            if st.button("Identify Condition", key="text_button"):
                if user_input:
                    with st.spinner("Processing... Please be patient."):
                        result = process_user_request(query=user_input)
                    if result:
                        display_results(result)
                else:
                    st.warning("Please enter your symptoms or medical condition.")
        else:
            uploaded_file = st.file_uploader("Upload any medical report for query ...", type=["jpg", "jpeg", "png"])
            if uploaded_file is not None:
                remove_old_uploads()
                image_path = os.path.join("uploads", uploaded_file.name)
                if not os.path.exists("uploads"):
                    os.makedirs("uploads")
                with open(image_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                with st.spinner("Processing image... Please be patient."):
                    result = process_user_request(image_path=image_path)
                if result:
                    display_results(result)

    add_footer()

def display_results(result):
    if isinstance(result, str):
        st.error(result)
    else:
        st.success(f"Identified Condition: {result['condition']}")
        
        temporary_text("DISCLAIMER: The information provided here is for educational purposes only and should not be considered medical advice. Always consult with a qualified healthcare professional before starting any treatment or taking any medication.")
        
        for remedy_type, info in result['remedies'].items():
            remedy_title = remedy_type.replace('_remedy', '').capitalize()
            with st.expander(f"{remedy_title} Remedies", expanded=True):
                st.markdown(f"""
                    <div class="scrollable-content">
                        {info['description']}
                    </div>
                """, unsafe_allow_html=True)
                if info['images']:
                    st.write("Remedy Images:")
                    cols = st.columns(len(info['images']))
                    for i, url in enumerate(info['images']):
                        with cols[i]:
                            st.image(url, width=200)
                else:
                    st.info("No images found for this remedy.")
        
        st.subheader("Expert Review")
        st.write(result['review'])

if __name__ == "__main__":
    main()