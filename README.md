# Korean GEC Noise Generator

> Research-driven synthetic error generation for Korean grammatical error correction (GEC).

[![Python 3.7+](https://img.shields.io/badge/Python-3.7%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-2ea44f.svg)](https://github.com/JKJIN1999/gec_noise_generator_ko/blob/master/LICENSE)

[English](#english) · [한국어](#한국어)

![Example output from the Korean GEC Noise Generator](https://github.com/JKJIN1999/gec_noise_generator_ko/blob/master/src/gecnk/resources/examples.PNG?raw=true)

---

## English

### Overview

Korean GEC Noise Generator creates synthetic spelling and grammar errors from
clean Korean sentences. It is designed to augment training data for Korean
grammatical error correction models with mistakes inspired by commonly observed
native-speaker errors.

The generator supports two complementary ways to control noise:

- **Error aspect** — generate errors using annotation-oriented labels such as
  omission, malformed form, replacement, and addition.
- **Error category** — generate errors using linguistic mechanisms such as
  particle, affix, consonant, vowel, or spacing errors.

The project uses **MeCab** for Korean morphological analysis and writes the
generated source–target pairs and error annotations to JSON.

### Highlights

- Generates realistic synthetic errors from clean Korean text
- Supports both annotation aspects and linguistic error categories
- Records up to four selected error annotations per sentence
- Preserves the original sentence as the correction target
- Records error labels, word positions, and character offsets
- Splits large outputs across multiple JSON files

### Requirements

- Python 3.7 or later
- Linux, macOS, or Google Colab recommended
- MeCab through `python-mecab-ko`

> [!NOTE]
> The project has known compatibility issues with `python-mecab-ko` on native
> Windows. Use WSL, Linux, macOS, or Google Colab if installation fails.

### Installation

```bash
git clone https://github.com/JKJIN1999/gec_noise_generator_ko.git
cd gec_noise_generator_ko

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

The main dependencies are `python-mecab-ko`, `g2pK`, `hangul-jamo`, `gensim`,
`fasttext`, and `wget`.

### Input format

Provide a UTF-8 text file containing **one correctly written Korean sentence per
line**:

```text
국내에서 유일하게 법정 커버드본드를 발행할 수 있는 주택금융공사는 지난해 7월 아시아 최초로 5억 달러 규모의 커버드본드를 발행했다
롯데 선발 송승준은 한화 타선을 5회까지 1실점으로 봉쇄하고 시즌 13승째를 챙겼다
3개월 후 최고 국방회의에서 충칭 천도를 통보했다
```

[Download sample input data](https://drive.google.com/drive/folders/1eBqzHWf7fzjjOjDxApSO6rrV2hdBLSWQ?usp=sharing)

### Quick start

Create an output directory, then run the generator from the repository root:

```bash
mkdir -p results

python3 src/gecnk/main.py \
  -d ./data/corpus.txt \
  -b aspect \
  -e OM REP MIF \
  -r ./results/
```

> [!IMPORTANT]
> The output directory must already exist. Include a trailing `/` in the value
> passed to `-r`.

Run the built-in example with the default options:

```bash
python3 src/gecnk/main.py
```

Show CLI help:

```bash
python3 src/gecnk/main.py --help
```

### CLI reference

| Option | Description | Default |
| --- | --- | --- |
| `-h`, `--help` | Show the command-line help message | — |
| `-d DATA_PATH` | UTF-8 text file containing one clean sentence per line | `./src/gecnk/resources/test-tgt` |
| `-e ERROR [ERROR ...]` | One or more error labels to generate | `OM` |
| `-r OUTPUT_DIR` | Directory in which JSON files are written | `./src/results/` |
| `-m MAX_ITEMS` | Maximum number of sentence records per JSON file | `100000` |
| `-t TOKENIZER` | Tokenizer to use: `mecab` or `black` | `mecab` |
| `-b MODE` | Error-generation mode: `aspect` or `category` | `aspect` |
| `-l LABEL_TYPE` | Output label scheme for category mode: `benchmark` or `original` | `benchmark` |

Use `ALL` to combine every label available in the selected mode, or
`random_two` to sample two labels:

```bash
# Apply all error aspects
python3 src/gecnk/main.py -d ./data/corpus.txt -b aspect -e ALL -r ./results/

# Randomly select two linguistic error categories
python3 src/gecnk/main.py -d ./data/corpus.txt -b category -e random_two -r ./results/
```

### Error-generation modes

#### 1. Error aspect (`-b aspect`)

This mode follows annotation-oriented error labels.

| Label | Name | Description |
| --- | --- | --- |
| `OM` | Omission | Removes a form that should appear in a complete sentence, such as a particle or final consonant |
| `MIF` | Malformed form | Produces a non-standard inflection, spelling, particle, affix, consonant, or vowel form |
| `REP` | Replacement | Replaces a valid form with another lexical or grammatical form |
| `ADD` | Addition | Inserts or duplicates a form that should not appear |
| `S_ADD` | Spacing addition | Inserts an incorrect space inside an eojeol |
| `S_DEL` | Spacing deletion | Incorrectly joins adjacent eojeols |

Example:

```bash
python3 src/gecnk/main.py \
  -d ./data/corpus.txt \
  -b aspect \
  -e OM MIF S_DEL \
  -r ./results/
```

#### 2. Error category (`-b category`)

This mode selects the linguistic mechanism used to generate an error.

| Label | Category | Typical transformation |
| --- | --- | --- |
| `JS` | Particle (조사) | Delete or replace a Korean particle |
| `BS` | Adverb (부사) | Confuse forms such as `이/히` or `마저/마져` |
| `AF` | Affix (접사) | Confuse affix forms such as `율/률` or `양/량` |
| `G2P` | Grapheme-to-phoneme | Rewrite a form according to its pronunciation |
| `CO` | Consonant | Modify an onset or final consonant, including tensification-related patterns |
| `VO` | Vowel | Confuse commonly mixed vowels such as `ㅔ/ㅐ`, `ㅖ/ㅔ`, or `ㅙ/ㅚ` |
| `S_ADD` | Spacing addition | Insert an incorrect space |
| `S_DEL` | Spacing deletion | Remove a required space |

Example:

```bash
python3 src/gecnk/main.py \
  -d ./data/corpus.txt \
  -b category \
  -e JS CO VO \
  -l benchmark \
  -r ./results/
```

When category mode is selected, `-l` controls the intended output label scheme:

- `benchmark` — annotation-aspect labels (`OM`, `MIF`, `REP`, `ADD`, `S_ADD`,
  `S_DEL`)
- `original` — generator-category labels (`JS`, `BS`, `AF`, `G2P`, `CO`, `VO`,
  `S_ADD`, `S_DEL`)

For a more detailed taxonomy, see the
[error classification notes](https://fuchsia-trouser-5c6.notion.site/dcc5d8bc23dc493c91ece7bd23dfb655).

### Output

The generator writes one or more UTF-8 JSON files to the selected output
directory. Each sentence record contains:

- `id` — sentence identifier
- `source` — sentence with synthetic errors
- `target` — original clean sentence
- `word` — word-level text and character offsets
- `GEC` — generated error spans, corrections, and labels

Illustrative structure:

```json
[
  {
    "id": "corpus.txt.0",
    "source": "노이즈가 적용된 문장",
    "target": "올바른 원문 문장",
    "word": [
      {
        "id": 0,
        "source": "노이즈가",
        "begin": 0,
        "end": 4
      }
    ],
    "GEC": [
      {
        "id": 0,
        "source": "오류 표현",
        "target": "정답 표현",
        "label": "MIF",
        "begin": 0,
        "end": 4
      }
    ]
  }
]
```

[View generated sample data](https://drive.google.com/drive/folders/163qe9Hec8gkgAE0ZzJmy-ryYLUpqcj-Y?usp=sharing)

### Tokenizers

`mecab` is the default and recommended tokenizer. For MeCab part-of-speech
tags, see this
[Korean MeCab POS tag reference](https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=aramjo&logNo=221404488280).

The `black` tokenizer option requires a separately obtained `wisekmapy` package
inside the repository. Because the generator was developed around MeCab,
tokenization or token-joining issues may occur with `black`.

### License

This project is released under the
[MIT License](https://github.com/JKJIN1999/gec_noise_generator_ko/blob/master/LICENSE).

Questions and bug reports are welcome in
[GitHub Issues](https://github.com/JKJIN1999/gec_noise_generator_ko/issues).

---

## 한국어

### 소개

Korean GEC Noise Generator는 올바른 한국어 문장에 인공적인 맞춤법·문법
오류를 생성하는 도구입니다. 한국인이 자주 범하는 오류를 바탕으로 한국어 문법
오류 교정(Grammatical Error Correction, GEC) 모델의 학습 데이터를 증강하도록
설계했습니다.

노이즈 생성 기준은 두 가지입니다.

- **오류 양상(Error aspect)** — 누락, 오형태, 대치, 첨가 등 주석 체계
  중심으로 오류를 생성합니다.
- **오류 유형(Error category)** — 조사, 접사, 자음, 모음, 띄어쓰기 등
  언어학적 변환 방식 중심으로 오류를 생성합니다.

한국어 형태소 분석에는 **MeCab**을 사용하며, 생성한 오류 문장과 원문 및 오류
주석은 JSON 파일로 저장합니다.

### 주요 기능

- 올바른 한국어 문장에서 자연스러운 합성 오류 생성
- 오류 양상과 언어학적 오류 유형의 두 가지 생성 기준 지원
- 문장당 최대 4개의 선택된 오류 주석 기록
- 올바른 원문을 교정 정답으로 보존
- 오류 라벨, 어절 위치, 문자 단위 오프셋 기록
- 대용량 결과를 여러 JSON 파일로 분할 저장

### 실행 환경

- Python 3.7 이상
- Linux, macOS 또는 Google Colab 권장
- `python-mecab-ko`를 통한 MeCab 사용

> [!NOTE]
> 네이티브 Windows 환경에서는 `python-mecab-ko` 호환성 문제가 발생할 수
> 있습니다. 설치에 실패하면 WSL, Linux, macOS 또는 Google Colab을 사용하세요.

### 설치

```bash
git clone https://github.com/JKJIN1999/gec_noise_generator_ko.git
cd gec_noise_generator_ko

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

주요 의존성은 `python-mecab-ko`, `g2pK`, `hangul-jamo`, `gensim`,
`fasttext`, `wget`입니다.

### 입력 데이터 형식

UTF-8로 인코딩된 텍스트 파일에 **올바른 한국어 문장을 한 줄에 하나씩**
저장합니다.

```text
국내에서 유일하게 법정 커버드본드를 발행할 수 있는 주택금융공사는 지난해 7월 아시아 최초로 5억 달러 규모의 커버드본드를 발행했다
롯데 선발 송승준은 한화 타선을 5회까지 1실점으로 봉쇄하고 시즌 13승째를 챙겼다
3개월 후 최고 국방회의에서 충칭 천도를 통보했다
```

[입력 예시 데이터 내려받기](https://drive.google.com/drive/folders/1eBqzHWf7fzjjOjDxApSO6rrV2hdBLSWQ?usp=sharing)

### 빠른 시작

출력 폴더를 만든 뒤 저장소 루트에서 아래 명령을 실행합니다.

```bash
mkdir -p results

python3 src/gecnk/main.py \
  -d ./data/corpus.txt \
  -b aspect \
  -e OM REP MIF \
  -r ./results/
```

> [!IMPORTANT]
> 출력 폴더는 실행 전에 만들어 두어야 합니다. `-r`에 입력하는 경로 끝에는
> `/`를 포함하세요.

기본 옵션과 내장 예시 데이터로 실행하려면 다음 명령을 사용합니다.

```bash
python3 src/gecnk/main.py
```

CLI 도움말은 다음과 같이 확인할 수 있습니다.

```bash
python3 src/gecnk/main.py --help
```

### CLI 인자

| 옵션 | 설명 | 기본값 |
| --- | --- | --- |
| `-h`, `--help` | 명령행 도움말 출력 | — |
| `-d DATA_PATH` | 한 줄에 하나의 올바른 문장이 들어 있는 UTF-8 텍스트 파일 | `./src/gecnk/resources/test-tgt` |
| `-e ERROR [ERROR ...]` | 생성할 오류 라벨 하나 이상 | `OM` |
| `-r OUTPUT_DIR` | JSON 결과를 저장할 폴더 | `./src/results/` |
| `-m MAX_ITEMS` | JSON 파일 하나에 저장할 최대 문장 레코드 수 | `100000` |
| `-t TOKENIZER` | 사용할 토크나이저: `mecab` 또는 `black` | `mecab` |
| `-b MODE` | 오류 생성 기준: `aspect` 또는 `category` | `aspect` |
| `-l LABEL_TYPE` | category 모드의 출력 라벨 체계: `benchmark` 또는 `original` | `benchmark` |

선택한 모드의 모든 라벨을 조합하려면 `ALL`, 임의의 라벨 두 개를 선택하려면
`random_two`를 사용합니다.

```bash
# 모든 오류 양상 적용
python3 src/gecnk/main.py -d ./data/corpus.txt -b aspect -e ALL -r ./results/

# 언어학적 오류 유형 중 두 개를 무작위로 선택
python3 src/gecnk/main.py -d ./data/corpus.txt -b category -e random_two -r ./results/
```

### 오류 생성 모드

#### 1. 오류 양상 (`-b aspect`)

주석 체계 중심의 오류 라벨을 사용합니다.

| 라벨 | 이름 | 설명 |
| --- | --- | --- |
| `OM` | 누락 | 완전한 문장에 필요한 조사나 종성 등의 형태를 삭제 |
| `MIF` | 오형태 | 잘못된 활용, 철자, 조사, 접사, 자음 또는 모음 형태 생성 |
| `REP` | 대치 | 올바른 형태를 다른 어휘·문법 형태로 교체 |
| `ADD` | 첨가 | 불필요한 형태를 삽입하거나 중복 |
| `S_ADD` | 띄어쓰기 첨가 | 어절 내부에 잘못된 공백 삽입 |
| `S_DEL` | 띄어쓰기 삭제 | 서로 다른 어절 사이의 필요한 공백 삭제 |

사용 예시:

```bash
python3 src/gecnk/main.py \
  -d ./data/corpus.txt \
  -b aspect \
  -e OM MIF S_DEL \
  -r ./results/
```

#### 2. 오류 유형 (`-b category`)

오류를 만드는 언어학적 변환 방식을 선택합니다.

| 라벨 | 유형 | 대표적인 변환 |
| --- | --- | --- |
| `JS` | 조사 | 조사 삭제 또는 다른 조사로 교체 |
| `BS` | 부사 | `이/히`, `마저/마져` 등의 형태 혼동 |
| `AF` | 접사 | `율/률`, `양/량` 등의 형태 혼동 |
| `G2P` | 발음 기반 | 발음 나는 형태로 표기 변경 |
| `CO` | 자음 | 초성·종성 변환 및 된소리 관련 오류 생성 |
| `VO` | 모음 | `ㅔ/ㅐ`, `ㅖ/ㅔ`, `ㅙ/ㅚ` 등 혼동 |
| `S_ADD` | 띄어쓰기 첨가 | 잘못된 공백 삽입 |
| `S_DEL` | 띄어쓰기 삭제 | 필요한 공백 삭제 |

사용 예시:

```bash
python3 src/gecnk/main.py \
  -d ./data/corpus.txt \
  -b category \
  -e JS CO VO \
  -l benchmark \
  -r ./results/
```

category 모드에서는 `-l`로 의도한 출력 라벨 체계를 선택할 수 있습니다.

- `benchmark` — 오류 양상 라벨(`OM`, `MIF`, `REP`, `ADD`, `S_ADD`,
  `S_DEL`)
- `original` — 생성기 오류 유형 라벨(`JS`, `BS`, `AF`, `G2P`, `CO`, `VO`,
  `S_ADD`, `S_DEL`)

세부 분류 기준은
[오류 분류 노트](https://fuchsia-trouser-5c6.notion.site/dcc5d8bc23dc493c91ece7bd23dfb655)를
참고하세요.

### 출력

생성기는 지정한 폴더에 UTF-8 JSON 파일을 하나 이상 저장합니다. 각 문장
레코드에는 다음 정보가 포함됩니다.

- `id` — 문장 식별자
- `source` — 합성 오류가 적용된 문장
- `target` — 올바른 원문
- `word` — 어절별 텍스트와 문자 위치
- `GEC` — 오류 범위, 교정 표현, 라벨

구조 예시:

```json
[
  {
    "id": "corpus.txt.0",
    "source": "노이즈가 적용된 문장",
    "target": "올바른 원문 문장",
    "word": [
      {
        "id": 0,
        "source": "노이즈가",
        "begin": 0,
        "end": 4
      }
    ],
    "GEC": [
      {
        "id": 0,
        "source": "오류 표현",
        "target": "정답 표현",
        "label": "MIF",
        "begin": 0,
        "end": 4
      }
    ]
  }
]
```

[생성 결과 예시 보기](https://drive.google.com/drive/folders/163qe9Hec8gkgAE0ZzJmy-ryYLUpqcj-Y?usp=sharing)

### 토크나이저

기본값이자 권장 토크나이저는 `mecab`입니다. 품사 태그는
[한국어 MeCab 품사 태그 참고 자료](https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=aramjo&logNo=221404488280)에서
확인할 수 있습니다.

`black` 옵션을 사용하려면 별도로 확보한 `wisekmapy` 패키지를 저장소 내부에
배치해야 합니다. 이 프로젝트는 MeCab을 기준으로 개발되었으므로 `black`에서는
토큰화 또는 결합 과정에 문제가 발생할 수 있습니다.

### 라이선스

이 프로젝트는
[MIT License](https://github.com/JKJIN1999/gec_noise_generator_ko/blob/master/LICENSE)로
배포됩니다.

질문과 버그 제보는
[GitHub Issues](https://github.com/JKJIN1999/gec_noise_generator_ko/issues)에
남겨 주세요.
