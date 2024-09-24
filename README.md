# FriendlyClinic: AI Personalized Medical Assistant

FriendlyClinic is an innovative AI-powered medical assistant designed to provide personalized health information and remedies based on user-provided symptoms or medical reports. This project aims to bridge the gap between technology and healthcare, offering a user-friendly interface for preliminary medical guidance.
-[Live link](https://friendlyclinic.streamlit.app)

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [Social Impact](#social-impact)
- [Limitations and Future Improvements](#limitations-and-future-improvements)
- [Contributing](#contributing)
- [License](#license)
- [Disclaimer](#disclaimer)

## Features

- **Dual Input Methods**: 
  - Text-based symptom input
  - Image upload for medical reports (OCR-enabled)
- **AI-Powered Diagnosis**: Utilizes advanced NLP models to identify potential medical conditions
- **Comprehensive Remedy Suggestions**:
  - Home remedies
  - Ayurvedic remedies
  - Homeopathic remedies
  - Allopathic treatments
- **Visual Aid**: Fetches relevant remedy images from web searches
- **Expert Review**: AI-generated review of identified conditions and suggested remedies
- **User-Friendly Interface**: Built with Streamlit for a seamless user experience
- **Responsive Design**: Adapts to various screen sizes for mobile and desktop use

## Tech Stack

- Python 3.8+
- Streamlit
- Groq API (LLM integration)
- OCR.space API (Image to text conversion)
- DuckDuckGo Search API (Image fetching)
- Concurrent programming (ThreadPoolExecutor)

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/Sayan-Maity-Code/Deploy_medical_assistent_bot.git
   cd Deploy_medical_assistent_bot

2. Install required packages:
   ```bash
   pip install -r requirements.txt
4. Set up environment variables:
Create a `.env` file in the root directory with the following:
  LLAMA_API=your_groq_api_key
  OCR_API=your_ocr_space_api_key
6. Run the Streamlit app:
   ```bash
   streamlit run app.py
  

## Usage

1. Choose between text input or image upload.
2. For text input: Describe your symptoms or condition in the text area.
3. For image upload: Upload a clear image of your medical report.
4. Click "Identify Condition" to process your input.
5. Review the AI-generated diagnosis, remedies, and expert review.
6. Always consult with a healthcare professional before acting on any advice.

## Social Impact

1. **Improved Healthcare Accessibility**: Provides basic medical information to users in areas with limited healthcare access.
2. **Health Education**: Enhances user understanding of various medical conditions and treatment options.
3. **Reduced Healthcare Burden**: Potentially decreases unnecessary doctor visits for minor ailments.
4. **Holistic Approach**: Promotes awareness of alternative medicine alongside conventional treatments.
5. **Empowerment**: Enables users to make more informed decisions about their health.
6. **Time and Cost Efficiency**: Offers quick, preliminary health guidance without the need for immediate doctor visits.
7. **Global Reach**: Can be accessed from anywhere, breaking geographical barriers to health information.

## Limitations and Future Improvements

1. **Accuracy Enhancement**:
- Integrate multiple AI models for cross-verification
- Implement continuous learning from user feedback and expert validation

2. **Data Privacy and Security**:
- Implement end-to-end encryption for all user data
- Obtain relevant data protection certifications (e.g., HIPAA compliance)

3. **Regulatory Compliance**:
- Collaborate with legal experts to ensure adherence to healthcare regulations
- Clearly communicate the app's limitations and non-diagnostic nature

4. **Multilingual Support**:
- Implement NLP models for multiple languages
- Provide culturally appropriate health information

5. **Offline Functionality**:
- Develop a lightweight offline mode for basic functionalities
- Implement sync capabilities for seamless online-offline transitions

6. **User Feedback Integration**:
- Create a robust feedback loop for continuous improvement
- Implement a rating system for suggested remedies

7. **Regular Updates**:
- Establish partnerships with medical institutions for up-to-date information
- Automate the process of integrating the latest medical research

8. **Accessibility Features**:
- Implement screen reader support and voice commands
- Ensure compliance with WCAG guidelines

9. **Integration with Wearables**:
- Incorporate data from fitness trackers and smartwatches for more accurate assessments

10. **Telemedicine Integration**:
 - Partner with telemedicine providers for seamless handoff to professional consultations

11. **Personalized Health Tracking**:
 - Implement user profiles for tracking health history and providing personalized advice

12. **Community Features**:
 - Create moderated forums for users to share experiences and support each other

## Contributing

We welcome contributions to FriendlyClinic! Please follow these steps:

1. Fork the repository
2. Create a new branch: `git checkout -b feature-branch-name`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-branch-name`
5. Submit a pull request

For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License .

## Disclaimer

FriendlyClinic is for educational and informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition. Never disregard professional medical advice or delay in seeking it because of something you have read on this website.

The use of this website does not create a doctor-patient relationship. FriendlyClinic does not practice medicine and does not dispense medical advice. If you are experiencing a medical emergency, please call your local emergency services immediately.
