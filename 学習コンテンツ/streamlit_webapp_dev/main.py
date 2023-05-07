import streamlit as st
import numpy as np
import time
import pandas as pd
from PIL import Image



st.title('お試し作成アプリ')
st.write('🐹健康管理表')




option = st.selectbox(
	'please choose your number',
	list(range(1,11))
)


df = pd.DataFrame(
	np.random.rand(100,2)/[50,50]+[34.7295, 135.3193],
	columns=['lat','lon']
	)



st.dataframe(df.style.highlight_max(axis=0))
#st.table(df.style.highlight_max(axis=0))
#st.line_chart(df)

st.area_chart(df)

st.map(df)

st.write('display Image')


if st.checkbox('Show Image'):
	img = Image.open('live.jpg')
	st.image(img, caption='pipi', use_column_width=True)

option = st.selectbox(
	'Select the number what you like.',
	list(range(1,11))
	)

st.write('Your faborite bumber is {}.'.format(option))

ham_name = st.text_input('please tell me your hamster`s name.')
st.write('Your hamster`s name is {}.'.format(ham_name))

ham_condition = st.slider('How many grams does your hamster weigh this week?', 0, 150, 50)
st.write('Your hamster`s wight is {}g.'.format(ham_condition))






"""
# 章

## 節

### 項


'''python
import streamlit as st
import numpy as np
imporrt pandas as pd
'''

"""


st.write('Downloading historical health data for your 🐹.(It is dummy)')

latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
	latest_iteration.text(f'Iteration{i+1}')
	bar.progress(i+1)
	time.sleep(0.01)

st.write('Completed! (It is dummy)')
