from konstants import *
import cv2

class MarkingScheme():
    def __init__(self, img_path, test_id, endNumber, schemeOrPaper, mark_scheme=[]) -> None:
        super().__init__()
        self.endNumber = endNumber
        self.schemeOrPaper = schemeOrPaper
        self.test_id = test_id
        self.dep_code = ''
        self.index_number = ''
        self.img_path = img_path
        self.all_rows = all_rows
        self.columns = columns
        self.correct_answer_map = {}
        self.student_answer = []
        self.width = 209 * 4
        self.height = 303 * 4
        self.dim = (self.width, self.height)
        self.images = {}
        self.answer_index_guide = ['a', 'b', 'c', 'd', 'e', 'f']
        self.aca_year_guide = ['2020/2021', '2021/2022', '2022/2023', '2023/2024']
        self.aca_year = ''
        self.dep_code_vert_loc = dep_code_vert_loc
        self.dep_code_hor_loc = dep_code_hor_loc
        self.idx_hor_loc = idx_hor_loc
        self.aca_year_loc = aca_year_loc
        self.mark_scheme = mark_scheme
        self.score = 0

    def binarize_image(self):
        img = cv2.imread(self.img_path)

        resized = cv2.resize(img, self.dim, interpolation=cv2.INTER_AREA)

        self.images['notimg'] = cv2.threshold(cv2.cvtColor(cv2.bitwise_not(resized), cv2.COLOR_BGR2GRAY), 0, 255,
                                              cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        # cv2_imshow(self.images['notimg'])

        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        # self.images['gray'] = gray
        del (resized)
        # smoothing
        blurred = cv2.GaussianBlur(gray, (11, 9), cv2.BORDER_DEFAULT)

        # thresh_gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        # cv2_imshow(thresh_gray)
        # self.images['thresh_gray'] = thresh_gray

        del (gray)
        # del(thresh_gray)

        # cv2_imshow(blurred)

        # thresholding
        thresh_blurred = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        # cv2_imshow(thresh_blurred)
        self.images['thresh_blurred'] = thresh_blurred

        del (blurred)
        del (thresh_blurred)

    def markForMe(self):
        if self.schemeOrPaper:
            self.get_correct_answers_map(start=1, end=self.endNumber)
        else:
            self.mark_scheme = sorted(self.mark_scheme, key=lambda d: d['answer_to'])
            self.get_correct_answers_map_student_answers(end=self.endNumber, start=1)

    def get_correct_answers_map(self, end, start=1):
        # self.P_or_g_or_none()
        for i in range(start, int(end) + 1, 1):
            answer = self.get_correct_answer_to_question(question_number=i)
            self.mark_scheme.append({
                'answer_to': i,
                'answer': answer
            })

    def get_correct_answers_map_student_answers(self, end, start=1):
        # self.P_or_g_or_none()
        for i in range(start, end + 1, 1):
            answer = self.get_correct_answer_to_question(question_number=i)
            self.student_answer.append({
                'answer_to': i,
                'answer': answer,
                'correct_answer': self.mark_scheme[i - 1]
            })
            if answer == self.mark_scheme[i - 1]['answer']:
                self.score += 1

    def post_mark_scheme(self):
        {
            'test_id': self.test_id,
            # 'number_of_questions':number_before_first_f
            'answers': self.mark_scheme
        }

    def P_or_g_or_none(self):
        p = self.images['thresh_gray'][p_g['p']['vertical'][0]:p_g['p']['vertical'][1],
            p_g['p']['horizontal'][0] + 1:p_g['p']['horizontal'][1] - 1]
        g = self.images['thresh_gray'][p_g['g']['vertical'][0]:p_g['g']['vertical'][1],
            p_g['g']['horizontal'][0] + 1:p_g['g']['horizontal'][1] - 1]
        g = cv2.bitwise_not(g)

        # cv2_imshow(p)
        # cv2_imshow(g)

        print(sum(sum(p)), sum(sum(g)))

    def get_correct_answer_to_question(self, question_number):
        row = self.all_rows[str(question_number)]
        column = self.columns[row['column']]
        # thresh_blurred[int(131.75*4):int(135.25*4), int(20*4):int(23*4)]
        a = self.images['thresh_blurred'][row['vertical_up']:row['vertical_down'],
            column['a'][0] + 1:column['a'][1] - 1]
        b = self.images['thresh_blurred'][row['vertical_up']:row['vertical_down'],
            column['b'][0] + 1:column['b'][1] - 1]
        c = self.images['thresh_blurred'][row['vertical_up']:row['vertical_down'],
            column['c'][0] + 1:column['c'][1] - 1]
        d = self.images['thresh_blurred'][row['vertical_up']:row['vertical_down'],
            column['d'][0] + 1:column['d'][1] - 1]
        e = self.images['thresh_blurred'][row['vertical_up']:row['vertical_down'],
            column['e'][0] + 1:column['e'][1] - 1]
        answers = [sum(sum(a)), sum(sum(b)), sum(sum(c)), sum(sum(d)), sum(sum(e))]
        correct_ans = answers.index(max(answers))
        return self.answer_index_guide[correct_ans]

    def odd_code(self, i):
        # looking for most white
        # (191, 196)(66, 69)
        arr = []
        for j in range(10):
            arr.append(
                sum(sum(
                    # cv2.bitwise_not(
                    self.images['notimg'][self.dep_code_vert_loc[j][0]:self.dep_code_vert_loc[j][1],
                    self.dep_code_hor_loc[i][0] + 1:self.dep_code_hor_loc[i][1] - 1]
                    #               )
                ))
            )
            # cv2_imshow(
            #     self.images['notimg'][ dep_code_vert_loc[j][0]:dep_code_vert_loc[j][1],
            #                                   dep_code_hor_loc[i][0]+1:dep_code_hor_loc[i][1]-1]
            # )

        return str(arr.index(min(arr)))

    def even_code(self, i):
        # looking for most black
        # (191, 196)(66, 69)
        arr = []
        for j in range(10):
            arr.append(
                sum(sum(
                    cv2.bitwise_not(self.images['notimg'][self.dep_code_vert_loc[j][0]:self.dep_code_vert_loc[j][1],
                                    self.dep_code_hor_loc[i][0]:self.dep_code_hor_loc[i][1]])
                ))
            )
            # cv2_imshow(
            #     self.images['thresh_blurred'][ dep_code_vert_loc[j][0]:dep_code_vert_loc[j][1],
            #                                   dep_code_hor_loc[i][0]+1:dep_code_hor_loc[i][1]-1]
            # )

        return str(arr.index(max(arr)))

    def odd_idx(self, i):
        # looking for most white
        # (191, 196)(66, 69)
        arr = []
        for j in range(10):
            arr.append(
                sum(sum(
                    # cv2.bitwise_not(
                    self.images['notimg'][self.dep_code_vert_loc[j][0] - 3:self.dep_code_vert_loc[j][1] + 3,
                    self.idx_hor_loc[i][0] + 1:self.idx_hor_loc[i][1] - 1]
                    #               )
                ))
            )

            # cv2_imshow(
            #     self.images['notimg'][ self.dep_code_vert_loc[j][0]:self.dep_code_vert_loc[j][1],
            #                                   self.idx_hor_loc[i][0]+1:self.idx_hor_loc[i][1]-1]
            # )

        return str(arr.index(min(arr)))

    def even_idx(self, i):
        # looking for most black
        # (191, 196)(66, 69)
        arr = []
        for j in range(10):
            arr.append(
                sum(sum(
                    cv2.bitwise_not(self.images['notimg'][self.dep_code_vert_loc[j][0]:self.dep_code_vert_loc[j][1],
                                    self.idx_hor_loc[i][0]:self.idx_hor_loc[i][1]])
                ))
            )

        return str(arr.index(max(arr)))

    def odd_aca_year(self, i):
        val = sum(sum(
            cv2.bitwise_not(
                self.images['notimg'][self.aca_year_loc['vert'][i][0] - 2:self.aca_year_loc['vert'][i][1] + 2,
                self.aca_year_loc['hor'][0] + 1:self.aca_year_loc['hor'][1] - 1
                ]
            )
        ))
        # cv2_imshow(
        #     cv2.bitwise_not(
        #     self.images['notimg'][ self.aca_year_loc['vert'][i][0]-2:self.aca_year_loc['vert'][i][1]+2,
        #                                       self.aca_year_loc['hor'][0]+1:self.aca_year_loc['hor'][1]-1
        #                       ]
        #     )
        # )
        return val

    def even_aca_year(self, i):
        val = sum(sum(
            cv2.bitwise_not(
                self.images['notimg'][self.aca_year_loc['vert'][i][0] - 2:self.aca_year_loc['vert'][i][1] + 2,
                self.aca_year_loc['hor'][0] + 1:self.aca_year_loc['hor'][1] - 1
                ]
            )
        ))

        # cv2_imshow(
        #     cv2.bitwise_not(
        #         self.images['notimg'][ self.aca_year_loc['vert'][i][0]-2:self.aca_year_loc['vert'][i][1]+2,
        #                                       self.aca_year_loc['hor'][0]+1:self.aca_year_loc['hor'][1]-1
        #                       ]
        #                     )
        # )
        return val

    def retrieve_aca_year(self):
        years = []
        for i in range(4):
            if i % 2 == 0:
                years.append(self.odd_aca_year(i))
            else:
                years.append(self.even_aca_year(i))
        self.aca_year = self.aca_year_guide[years.index(max(years))]

    def retrieve_dep_code(self):
        code = ''
        for i in range(3):
            if i % 2 == 0:
                code += self.odd_code(i)  # horizontals
            else:
                code += self.even_code(i)  # horizontals
        self.dep_code = code
        # print(code)

    def retrieve_index_number(self):
        idx = ''
        for i in range(7):
            if i % 2 == 0:
                idx += self.odd_idx(i)  # horizontals
            else:
                idx += self.even_idx(i)  # horizontals
        self.index_number = idx

    def modularize_scheme_or_ans(self):
        if self.schemeOrPaper:
            return {
                'scheme': self.mark_scheme
            }
        else:
            return {
                'index_number': self.index_number,
                'answers': self.student_answer,
                'score': self.score,
                'out_of': len(self.mark_scheme)
            }


# if __name__=='__main__':
#     scheme = MarkingScheme(img_path='schema.jpg', test_id='1234', endNumber=40, schemeOrPaper=True)
#     scheme.binarize_image()
#     # scheme.get_correct_answers_map()
#     # scheme.retrieve_dep_code()
#     #scheme.retrieve_index_number()
#     #scheme.retrieve_aca_year()

#     scheme.markForMe()
#     print(scheme.modularize_schem_or_ans())
