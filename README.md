# Noise Generator for Korean Text Grammar Error Correction Model


# 설명

### 이 모델은 한글 맞춤법 검사기의 학습 데이터 증강을 목적으로 한국인이 자주 틀리는 오류 리서치에 기반해 생성한 노이즈 생성기입니다.
### 오류의 생성 방법에는 국립 국어원의 오류주석 양상을 기준으로 한 방법과 오류 유형을 기준으로 하는 두가지 방법이 있습니다.
### 형태소 분석기 Mecab을 활용하고 있습니다.
품사 태그는 아래의 사이트를 방문해 확인하시길 바랍니다.<br />
https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=aramjo&logNo=221404488280 <br />

# 결과물

![Alt text](src/gecnk/resources/examples.PNG?raw=true "Title")

# Requirements

## Python >= 3.7 

```consol
pip install wget
pip install hangul_jamo
pip install inko
pip install g2pk
pip install gensim
pip install python-mecab-ko
```
 현재 윈도우 os에서 python-mecab-ko가 실행되지 않는 오류가 있습니다.<br />
 리눅스나 구글 코랩 macos에서만 사용 가능합니다.<br />

# 사용 방법
## 준비 자료

```consol
git clone https://github.com/JKJIN1999/gec_noise_generator_ko.git
```

GEC noise generator ko 에는 7가지 인자를 받습니다.

터미널 또는 bash에서 아래 코드에 원하는 인자를 입력하여 사용할 수 있습니다.<br />
```consol
python3 gec_noise_generator_ko/src/gecnk/main.py 
```
뒤에 인자를 입력하시면 됩니다. 예시는 아래와 같이<br />
```consol
python3 gec_noise_generator_ko/src/gecnk/main.py -e OM REP MIF -r ./src/results -d NWRW
```
## Arguments<br />
* -h, help            
> README.md 에 자세한 설명이 적혀져있습니다.<br />
* -d data_directory     
> 오류를 생성할 데이터 경로를 입력하시오<br />
* -e error_list [error_list ...]<br />
> 생성할 오류 리스트를 입력하시오<br />
* -r result_directory   
> 파일을 저장할 경로를 입력하시오<br />
> 기본 저장 경로는 src/gecnk/results/ 입니다<br />
* -m json_maximum      
> 한 파일에 저장할 최대 json 리시트 갯수를 입력하시오<br />
> 기본 100000개의 json 리스트로 설정되어있습니다<br />
* -t tokenizer_type    
> 원하는 토크나이저의 유형을 -t 뒤에 입력하십시오<br />
> 기본 토크나이저는 mecab으로 설정되어있습니다<br />
> black은 wisekmapy를 보유하시고 gec_noise_generator_ko 파일 안에 위치한다면 사용이 가능하지만<br /> 
> mecab을 토대로 개발되었기 때문에 결합과정에서 오류가 존재함으로 mecab을 권장드립니다. <br />
* -b error_by      
> 오류 생성 기준을 오류 양상으로 할것인지 오류 유형으로 할것인지 입력하시오<br />
> aspect는 오류 양상을 기준으로 오류 생성 (JS, BS, AF, G2P, S_ADD, S_DEL, CO, VO)<br />
> category는 오류 유형을 기준으로 오류 생성 (OM REP MIF ADD S_ADD S_DEL)<br />
> 만약 aspect를 고르셨다면 -l label_type은 설정하지 않아도 괜찮습니다 (JS, BS, AF, G2P, S_ADD, S_DEL, CO, VO)<br />
> 기본 error_by는 category로 설정되어있습니다<br />
* -l label_type        
> 원하는 Label 타입을 입력하시오 <br />
> 기본 Label 타입은 benchmark로 설정되어있습니다<br />
> original로 설정하시면 결과 라벨을 오류 유형으로 나타냅니다 (JS, BS, AF, G2P, S_ADD, S_DEL, CO, VO)<br />
> benchmark로 설정하시면 결과 라벨을 국립 국어원 오류 양상으로 나타냅니다 (OM REP MIF ADD S_ADD S_DEL) <br />

결과물인 Json 파일은 기본적으로 result 폴더안에 저장되어있습니다. 

gec_noise_generator_ko 를 사용하기 위해서는 텍스트 파일과 그 경로가 필요합니다.<br />
텍스트 데이터는 줄단위로 문장이 나누어진 형태여야만 합니다.<br />

# 오류 유형별 오류 생성 방법 (Error Category) 
### 정확한 분류 기준은 아래의 링크를 참조
### https://fuchsia-trouser-5c6.notion.site/dcc5d8bc23dc493c91ece7bd23dfb655

* JS [josa Error]
> 품사가 조사인 어절을 삭제한다<br />
> 조사 변경 기준표에 따라 조사를 변경한다. 아래의 링크를 참조<br />

* BS [busa error]
> 부사 ["이", "히"] 로 변경한다<br />
> 부사 ["마저", "마져"] 로 변경한다<br />

* CO [consonant error]
> 어절을 음절로, 음절을 음소로 나누어 자음을 변경한다<br />
> 사이시옷 오류<br />
> 같은 음절의 된소리가 반복될 경우 뒤의 음절 초성을 예사소리로 변경<br />
> "으려"를 "을려"로 변경 또한 "려고"앞 음절에 "ㄹ"종성 추가<br />
> 소리 나는대로 종성을 변경<br />
> ["않", "안]" 또는 ["많", "만"] 으로 종성 변경<br />
> 종성 "ㅎ" 탈락<br />

* VO [vowel error]
> 단모음 ["ㅔ", "ㅐ"] 교체<br />
> 이중모음 ["ㅖ", "ㅔ"], ["ㅢ", "ㅣ"], ["ㅙ", "ㅚ"] 변경<br />

* S_ADD [spacing add error]
> 앞 형태소가 접사이고 <br />
> 뒤의 형태소가 조사거나 (명사,동사,형용사)파생 접미사인 경우 띄어쓰기를 생성 <br />


* S_DEL [spacing delete error]
> 특정 기준에 따라 constant 파일에 있는 SPACING_DEL_DIC을 활용<br />
> 앞의 형태소가 key이고 뒤의 형태소가 value안에 있는경우 두 어절을 붙여쓴다<br />

* ALL
> 모든 오류유형을 결합하여 오류를 생성<br />

* random_two
> 랜덤하게 두가지 오류를 골라서 오류를 생성<br />

# 오류 양상별 오류 생성 방법 (Error Aspect) 

* OM [누락]
> 완전한 문장/발화에서 나타나야 할 형태가 빠져있는 경우<br />
> Josa: [조사 전체 삭제, 조사 일부분 삭제]<br />
> Consonant: [사이시옷 삭제, 종성 “ㅎ” 삭제]<br />

* MIF [오형태]
> 한국어에 존재하지 않는 어휘를 만들어 내거나 조사와 어미의 활용 형태가 잘못된 경우 즉, 활용 또는 곡용을 잘못하여 다른 이형태를 사용한 경우 또는 철자를 잘못 사용한 경우<br />
> Consonant: [두음법칙, 겹처나는 된소리 예사소리로 교체, 종성을 같은 소리인 다른 종성으로 교체, 종성 “ㄶ“과”ㄴ”의 교체, ] <br />
> Vowel: [단모음 “ㅔ” 와 “ㅐ 교체,  이중모음 “ㅖ” 와 “ㅔ” 또는 “ㅙ” 와 “ㅚ” 교체]<br />
> Josa: [같은 길이의 조사 (이>가, 에>께, 에>의, 처럼>마냥)을 제외한 모든 조사 변경]<br />
> Affix: [”율” 와 “률” 교체 또는 ”양” 와 “량” 교체]<br />
> Busa: [ “이” 와 “히” 교체, ”마져” 와 “마저” 교체]<br />
> Grapheme_to_Phonem: [g2pk 룰북 기준에 의해 소리 나는 대로 변경]<br />

* REP [대치]
> 다른 의미의 어휘를 사용하거나 적절한 품사를 사용하지 못한 경우 또는 한국어에 없는 표현이나 한국어가 아닌 다른 언어를 사용한 경우<br />
> Josa: [같은 길이의 조사 이>가, 에>께, 에>의, 처럼>마냥 교체]<br />
> Vowel: [이중모음 “의” 와 단모음 “이” 교체]<br />

* ADD [첨가]
> 완전한 문장/발화에서 나타나지 말아야 할 형태가 쓰인 경우나 중복된 형태를 반복해서 사용한 경우<br />
> Josa: [조사를 길게 변경]<br />
> Consonant: [종성에 “ㄹ” 추가]<br />

* S_DEL [spacing delete error]
> 특정 기준에 따라 constant 파일에 있는 SPACING_DEL_DIC을 활용<br />
> 앞의 형태소가 key이고 뒤의 형태소가 value안에 있는경우 두 어절을 붙여쓴다<br />

* S_ADD [spacing add error]
> 앞 형태소가 접사이고 <br />
> 뒤의 형태소가 조사거나 (명사,동사,형용사)파생 접미사인 경우 띄어쓰기를 생성 <br />

# 토크나이저 Black 활용
Black 또한 사용 가능하지만 추가적인 작업이 필요합니다.<br />
Black을 사용하고 싶으신 경우 wisekmapy를 gec_noise_generator_ko 파일 안에 넣어주시면 사용이 가능합니다.<br />
