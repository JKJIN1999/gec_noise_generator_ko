#! /usr/bin/python
# -*- coding: utf-8 -*-
import sys
import jpype
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from wisekmapy import jvm

__all__ = ['Wisekma']


class KmaResult(object):
    text = None
    token_list = None
    position_list = None
    start_pos = None

    def __init__(self, text, token_list, start_pos = None, position_list=None):
        self.text = text
        self.token_list = token_list
        self.start_pos = start_pos
        self.position_list = position_list


class Wisekma:
    """
    WISE KMA Black Python API class
    ** Default value of all tagging parameter in anlayze() is False.
    """

    def __init__(self, jvmpath=None, wkb_jar_file="wisekma-black-1.6.3-nl.jar"):
        # def __init__(self, jvmpath=None, wkb_jar_file="wisekma-black-1.3.6-M3-executable.jar"):
        """Constructor
        :param jvmpath: The path of the JVM. If left empty, inferred by :py:func:`jpype.getDefaultJVMPath`.
        :param wkb_jar_path: The path of the WISE KMA Black jar file.
        :return:
        """
        # start_time = time.time()

        if not jpype.isJVMStarted():
            jvm.init_jvm(jvmpath, wkb_jar_path=wkb_jar_file)

        knowledgePath = '%s%sknowledge' % (os.path.dirname(os.path.realpath(__file__)), os.sep)
        self.configPath = os.path.join(knowledgePath, 'config.yaml') # ''%s%sconfig.yaml' % (knowledgePath, os.sep)
        self.configPath = self.configPath.replace("\\", "/")

        # blackPackage = jpype.JPackage('kr.co.wisenut.nlp')
        blackAPI = jpype.JPackage('kr.co.wisenut.nlp.API')
        self.analyzer = blackAPI.WKB_Analyzer()
        ret = self.analyzer.initialize(self.configPath)
        if ret != 0:
            print('initialize %d' % ret)
            print('initialize %s' % self.configPath)
        self.analyzer.setCharset("utf-8")

        # print("Initialize time : %s" % (time.time() - start_time))

    def morph(self, phrase, nbest=None):
        """Extract morpheme candidates
        :param str phrase: text to analyze
        :param int nbest: nbest option(1 ~ 10)
        :return: morpheme candidates
        :rtype: list of list of tuple(list of tuple(str, str), float)
        """
        morph = []
        if nbest is None:
            tokens = self.analyzer.analyze(phrase, 5, True)
        else:
            tokens = self.analyzer.analyze(phrase, nbest, False)

        for i in range(tokens.size()):
            eojeols = []
            morphemeSetList = tokens.get(i).getMorphemeSetList()
            for j in range(morphemeSetList.size()):
                morphemeList = morphemeSetList.get(j).getMorphemeList()
                score = morphemeSetList.get(j).getProbability()
                eojeol = []
                for k in range(morphemeList.size()):
                    morpheme = morphemeList.get(k)
                    morph_tag = (morpheme.getMorphemeString(), morpheme.getStrPosTag())
                    eojeol.append(morph_tag)
                eojeols.append((eojeol, score))
            morph.append(eojeols)
        return morph

    def nouns(self, phrase, nbest=None, tagging=None):
        """Extract nouns
        :param str phrase: text to analyze
        :param int nbest: nbest option(1 ~ 10)
        :param bool tagging: tagging option
        :return: nouns 
        :rtype: list str
        """
        nouns = set()

        if nbest is None or tagging is None:
            tokens = self.analyzer.analyze(phrase, 5, False)
        else:
            tokens = self.analyzer.analyze(phrase, nbest, tagging)

        for i in range(tokens.size()):
            morphemeSetList = tokens.get(i).getMorphemeSetList()
            for j in range(morphemeSetList.size()):
                morphemeList = morphemeSetList.get(j).getMorphemeList()
                for k in range(morphemeList.size()):
                    if "NN" in morphemeList.get(k).getStrPosTag() or "XR" in morphemeList.get(k).getStrPosTag():
                        nouns.add(morphemeList.get(k).getMorphemeString())
        return list(nouns)

    def pos(self, phrase, join=False):
        """POS tagger
        :param str phrase: text to analyze
        :param int nbest: nbest option(1 ~ 10)
        :param bool join: join morpheme, tag
        :return: result of pos tagging
        :rtype:
            join==True  : list of list of str
            join==False : list of list of tuple(str, str) 
        """
        morph = []
        tokens = self.analyzer.analyze(phrase)

        for i in range(tokens.size()):
            morphemeSetList = tokens.get(i).getMorphemeSetList()
            for j in range(morphemeSetList.size()):
                morphemeList = morphemeSetList.get(j).getMorphemeList()
                for k in range(morphemeList.size()):
                    morpheme = morphemeList.get(k).getMorphemeString()
                    tag = morphemeList.get(k).getStrPosTag()
                    if join:
                        morph.append(morpheme + '/' + tag)
                    else:
                        morph.append((morpheme, tag))
        return morph

    def analyze_document(self, document):
        res_arr = self.analyzer.documentAnalyze(document)
        results = []
        for res in res_arr:
            text = res.getSentenceText()
            start_pos = res.getStartPosition()
            token_list = []
            position_arr = []
            tokens = res.getAnalyzed()
            for i in range(tokens.size()):
                morphemeSetList = tokens.get(i).getMorphemeSetList()
                for j in range(morphemeSetList.size()):
                    morphemeList = morphemeSetList.get(j).getMorphemeList()
                    for k in range(morphemeList.size()):
                        morpheme = morphemeList.get(k).getMorphemeString()
                        tag = morphemeList.get(k).getStrPosTag()
                        token_list.append(morpheme + '/' + tag)
                        position_arr.append(morphemeList.get(k).getStartOffset())
            results.append(KmaResult(text, token_list, start_pos, position_arr))

        return results

    def analyze_sentence(self, sentence):
        morph = []
        pos_arr = []
        tokens = self.analyzer.analyze(sentence)

        for i in range(tokens.size()):
            morphemeSetList = tokens.get(i).getMorphemeSetList()
            for j in range(morphemeSetList.size()):
                morphemeList = morphemeSetList.get(j).getMorphemeList()
                for k in range(morphemeList.size()):
                    morpheme = morphemeList.get(k).getMorphemeString()
                    tag = morphemeList.get(k).getStrPosTag()
                    morph.append(morpheme + '/' + tag)
                    pos_arr.append(morphemeList.get(k).getStartOffset())

        return morph, pos_arr
        # res = self.analyzer.sentenceAnalyze(sentence)
        # pos_arr = []
        # morphemes = []
        # for item in res.split(' '):
        #     idx = item.rindex('#')
        #     pos_arr.append(int(item[idx+1:]))
        #     morphemes.append(item[:idx])
        # return morphemes, pos_arr


    def split_document(self, document):
        res_arr = self.analyzer.split(document)
        results = []
        for res in res_arr:
            results.append(res.getSentenceText())
        return results

    def ret(self, phrase, join=False):
        """POS tagger
        :param str phrase: text to analyze
        :param int nbest: nbest option(1 ~ 10)
        :param bool join: join morpheme, tag
        :return: result of pos tagging
        :rtype:
            join==True  : list of list of str
            join==False : list of list of tuple(str, str)
        """
        ret = {}
        morph_info = {}
        morph_info_list = []
        morph_list = []
        position_list = []
        sentences = []
        if isinstance(phrase, list):
            for sentence in phrase:
                sentences.append(self.analyzer.analyze(sentence, 5, True))
        else:
            sentences.append(self.analyzer.analyze(phrase, 5, True))

        last_offset = 0
        for tokens in sentences:
            for token in tokens:
                for morphemeSet in token.getMorphemeSetList():
                    for i, morpheme in enumerate(morphemeSet.getMorphemeList()):
                        morpheme_str = morpheme.getMorphemeString()
                        tag_str = morpheme.getStrPosTag()

                        morph_info['lemma'] = morpheme_str
                        morph_info['tag'] = tag_str
                        morph_info['offset'] = last_offset + morpheme.getStartOffset()
                        morph_info_list.append(morph_info)
                        position_list.append(last_offset + morpheme.getStartOffset())
                        morph_info = {}
                        if join:
                            morph_list.append(morpheme_str + '/' + tag_str)
                        else:
                            morph_list.append((morpheme_str, tag_str))
            last_offset = morph_info_list[-1]['offset'] + 1

        ret['det'] = morph_info_list
        ret['morph_list'] = morph_list
        ret['position_list'] = position_list
        return ret

    def ret_answer(self, start_index, end_index, phrase, join=False):
        """POS tagger
        :param str phrase: text to analyze
        :param int nbest: nbest option(1 ~ 10)
        :param bool join: join morpheme, tag
        :return: result of pos tagging
        :rtype:
            join==True  : list of list of str
            join==False : list of list of tuple(str, str)
        """
        if start_index != -1 and end_index != -1:
            phrase = phrase[:start_index] + '◙' + phrase[start_index:end_index] +'◙' + phrase[end_index:]
        ret = {}
        morph_list = []
        position_list = []
        answer_begin = answer_end = -1
        is_answer = False
        tokens = self.analyzer.analyze(phrase, 5, True)

        i = 0
        for token in tokens:
            for morphemeSet in token.getMorphemeSetList():
                for morpheme in morphemeSet.getMorphemeList():
                    morpheme_str = morpheme.getMorphemeString()
                    tag_str = morpheme.getStrPosTag()

                    if morpheme_str == '◙' and is_answer is True:
                        answer_end = i-1
                        is_answer = False
                    elif morpheme_str == '◙' and is_answer is False:
                        answer_begin = i
                        is_answer = True
                    else:
                        if join:
                            morph_list.append(morpheme_str + '/' + tag_str)
                        else:
                            morph_list.append((morpheme_str, tag_str))
                        position_list.append(token.getStartOffset())
                        i += 1

        ret['morph_list'] = morph_list
        ret['position_list'] = position_list
        ret['answer_begin'] = answer_begin
        ret['answer_end'] = answer_end
        return ret

    def setCharset(self, charset="utf-8"):
        """Set character set
        :param str charset: character set (utf-8 or cp949)
        :return:
        """
        self.analyzer.setCharset(charset)


if __name__ == "__main__":
    # if len(sys.argv) != 2:
    #     print('Cannot find WISE KMA Black jar file')
    #     print('usage: wisekma.py [WKB_JAR_FILE]')
    #     exit()

    # wkb_jar_file = sys.argv[1]

    wisekma = Wisekma()
    wisekma.setCharset("utf-8")

    # # Test 1: morph 메소드의 입력 파라미터별 테스트
    print(wisekma.morph("안녕하신가요"))
    print(wisekma.morph("안녕하신가요", nbest=5))
    #
    # # Test 2: nouns 메소드의 입력 파라미터별 테스트
    print(wisekma.nouns("안녕하신가요"))
    print(wisekma.nouns("안녕하신가요", nbest=5, tagging=False))
    print(wisekma.nouns("안녕하신가요", nbest=5, tagging=True))

    # # Test 3: pos 메소드의 입력 파라미터별 테스트
    # print(wisekma.pos("무궁화 꽃이 피었습니다."))
    # print(wisekma.pos("무궁화 꽃이 피었습니다."))
    # print(wisekma.pos("무궁화 꽃이 피었습니다.", join=True))

    # Test 4: ret 메소드 테스트
    # start_index = 304
    # answer_text = '초대 국무장관직'
    # end_index = start_index + len(answer_text)
    # ret =wisekma.ret_answer(start_index, end_index, "알렉산더 메이그스 헤이그 2세(영어: Alexander Meigs Haig, Jr., 1924년 12월 2일 ~ 2010년 2월 20일)는 미국의 국무 장관을 지낸 미국의 군인, 관료 및 정치인이다. 로널드 레이건 대통령 밑에서 국무장관을 지냈으며, 리처드 닉슨과 제럴드 포드 대통령 밑에서 백악관 비서실장을 지냈다. 또한 그는 미국 군대에서 2번째로 높은 직위인 미국 육군 부참모 총장과 나토 및 미국 군대의 유럽연합군 최고사령관이었다. 한국 전쟁 시절 더글러스 맥아더 유엔군 사령관의 참모로 직접 참전하였으며, 로널드 레이건 정부 출범당시 초대 국무장관직을 맡아 1980년대 대한민국과 미국의 관계를 조율해 왔다. 저서로 회고록 《경고:현실주의, 레이건과 외교 정책》(1984년 발간)이 있다.", join=True)

    # ret = wisekma.ret("알렉산더 메이그스 헤이그 2세(영어: Alexander Meigs Haig, Jr., 1924년 12월 2일 ~ 2010년 2월 20일)는 미국의 국무 장관을 지낸 미국의 군인, 관료 및 정치인이다. 로널드 레이건 대통령 밑에서 국무장관을 지냈으며, 리처드 닉슨과 제럴드 포드 대통령 밑에서 백악관 비서실장을 지냈다. 또한 그는 미국 군대에서 2번째로 높은 직위인 미국 육군 부참모 총장과 나토 및 미국 군대의 유럽연합군 최고사령관이었다. 한국 전쟁 시절 더글러스 맥아더 유엔군 사령관의 참모로 직접 참전하였으며, 로널드 레이건 정부 출범당시 초대 국무장관직을 맡아 1980년대 대한민국과 미국의 관계를 조율해 왔다. 저서로 회고록 《경고:현실주의, 레이건과 외교 정책》(1984년 발간)이 있다.", join=True)

    # ret = wisekma.pos("커닐링구스(커닐링거스, 쿤닐링구스, 영어: Cunnilingus)는 입술, 혀, 입 등의 모든 구강기관으로 여성의 성기를 애무하는 것을 말하며 구강성교(오럴섹스, 영어: Oral sex)라고도 한다. 보통 남성이 행하며 동성의 여성이 행하는 경우도 있다. 혀를 질에 넣거나 여성의 클리토리스, 외음부나 그 주변을 핥거나 빨아서 애무한다. 받는 사람이 다양한 성감을 느끼는 원인이 되며 특히 클리토리스의 감각이 매우 중요하다. 타액과 수성윤활제가 자주 사용되고 이것들은 부드럽게 매끄러운 자극을 가능하게 한다. 파트너의 반응에 귀를 기울이면서 손가락과 같은 다른 애무와 함께 몸 전체에 다양한 자극과 결합하여 양측이 폭넓은 즐거움을 나눌 수 있게 한다. 전희로서 하는 경우가 많지만, 오르가즘에의 도달 여부에 관계없이 커닐링구스 자체가 성행위이다.")

    # phrase = ['1839년 바그너는 괴테의 파우스트을 처음 읽고 그 내용에 마음이 끌려 이를 소재로 해서 하나의 교향곡을 쓰려는 뜻을 갖는다.',
    #           '이 시기 바그너는 1838년에 빛 독촉으로 산전수전을 다 걲은 상황이라 좌절과 실망에 가득했으며 메피스토펠레스를 만나는 파우스트의 심경에 공감했다고 한다.',
    #           '또한 파리에서 아브네크의 지휘로 파리 음악원 관현악단이 연주하는 베토벤의 교향곡 9번을 듣고 깊은 감명을 받았는데, 이것이 이듬해 1월에 파우스트의 서곡으로 쓰여진 이 작품에 조금이라도 영향을 끼쳤으리라는 것은 의심할 여지가 없다.',
    #           '여기의 라단조 조성의 경우에도 그의 전기에 적혀 있는 것처럼 단순한 정신적 피로나 실의가 반영된 것이 아니라 베토벤의 합창교향곡 조성의 영향을 받은 것을 볼 수 있다.',
    #           '그렇게 교향곡 작곡을 1839년부터 40년에 걸쳐 파리에서 착수했으나 1악장을 쓴 뒤에 중단했다.',
    #           '또한 작품의 완성과 동시에 그는 이 서곡(1악장)을 파리 음악원의 연주회에서 연주할 파트보까지 준비하였으나, 실제로는 이루어지지는 않았다.',
    #           '결국 초연은 4년 반이 지난 후에 드레스덴에서 연주되었고 재연도 이루어졌지만, 이후에 그대로 방치되고 말았다.',
    #           '그 사이에 그는 리엔치와 방황하는 네덜란드인을 완성하고 탄호이저에도 착수하는 등 분주한 시간을 보냈는데, 그런 바쁜 생활이 이 곡을 잊게 한 것이 아닌가 하는 의견도 있다.']
    # ret = wisekma.ret(phrase)
    ret = wisekma.split_document('알렉산더 메이그스 헤이그 2세(영어: Alexander Meigs Haig, Jr., 1924년 12월 2일 ~ 2010년 2월 20일)는 미국의 국무 장관을 지낸 미국의 군인, 관료 및 정치인이다. 로널드 레이건 대통령 밑에서 국무장관을 지냈으며, 리처드 닉슨과 제럴드 포드 대통령 밑에서 백악관 비서실장을 지냈다. 또한 그는 미국 군대에서 2번째로 높은 직위인 미국 육군 부참모 총장과 나토 및 미국 군대의 유럽연합군 최고사령관이었다. 한국 전쟁 시절 더글러스 맥아더 유엔군 사령관의 참모로 직접 참전하였으며, 로널드 레이건 정부 출범당시 초대 국무장관직을 맡아 1980년대 대한민국과 미국의 관계를 조율해 왔다. 저서로 회고록 《경고:현실주의, 레이건과 외교 정책》(1984년 발간)이 있다.')
    for sent in ret:
        print(sent)

