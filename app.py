import streamlit as st
import numpy as np
from PIL import Image
import easyocr

harmful_e_numbers = {
    "E407": "Карагенан (възпаления, храносмилателни проблеми)",
    "E621": "Натриев глутамат (главоболие, алергии)",
    "E262": "Натриев ацетат (дразни стомаха)",
    "E300": "Аскорбинова киселина (в големи дози дразни стомаха)",
    "E330": "Лимонена киселина (уврежда зъбния емайл)",
    "E250": "Натриев нитрит (риск от онкологични заболявания)",
    "E952": "Цикламат подсладител",
    "E471": "Емулгатор",
    "E472": "Емулгатор",
    "E110": "Сънсет жълто FCF",
    "E304": "Аскорбил палмитат",
    "E422": "Глицерол (глицерин)",
    "E470a": "Натриеви, калиеви и калциеви соли на мастни киселини",
    "E102": "Тартразин",
    "E132": "Индигокармин",
    "E924": "Калиев бромат",
    "E151": "Брилянтно черно BN",
    "E210": "Бензоена киселина",
    "E296": "Ябълчена киселина",
    "E310": "Пропил галат",
    "E320": "Бутилхидроксианизол",
    "E322": "Лецитин",
    "E553b": "Талк",
    "E440": "Пектин",
    "E421": "Манитол"
}

@st.cache_resource
def load_ocr_model():
    return easyocr.Reader(['en'], gpu=False)

reader = load_ocr_model()

st.title("🧪 Food Chemistry Scanner")
st.write("Upload an ingredient label to analyze chemical additives.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
   
    st.image(image, caption='Uploaded Label', use_container_width=True) 
    
    image_np = np.array(image)
    
    with st.spinner("Analyzing ingredients..."):
        results = reader.readtext(image_np)
        
        extracted_text = " ".join([res[1] for res in results]).upper() 
        
    st.subheader("Extracted Ingredient Text:")
    st.info(extracted_text)

   
    found_chemicals = [chem for chem in harmful_e_numbers if chem in extracted_text]
    
    if found_chemicals:
        st.warning(f"⚠️ Potential chemical additives found: {', '.join(found_chemicals)}")
       
        for chem in found_chemicals:
            st.write(f"**{chem}**: {harmful_e_numbers[chem]}")
    else:
        st.success("No common additives from the watchlist detected.")

        st.success("No common additives from the watchlist detected.")

