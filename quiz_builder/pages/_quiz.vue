<template>
    <v-layout justify-center class="mt-3 mb-5">
        <v-flex xs8>
            <h1 class="display-1">{{ quiz.quizTitle }}</h1>
            <p>You can select multiple options. Right click to de-select an option.</p>
            <v-card v-for="(question, index1) in quiz.questions" :key="index1" class="mt-4">
                <v-card-title class="deep-purple white--text">
                    <h1 class="headline">{{ question }}</h1>
                </v-card-title>
                <v-card-text>
                    <v-container>
                        <v-radio-group row style="display: block;" v-model="correct[index1]" multiple>
                            <v-radio v-for="(correctId, index2) in convert(quiz.options[index1].length)" :key="index2" class="ml-16" :value="'Option ' + correctId" color="green" :label="quiz.options[index1][index2]" @mouseup="reset(correctId, index1)"></v-radio>
                        </v-radio-group>
                    </v-container>
                </v-card-text>
            </v-card>
            <v-btn color="purple darken-2" dark small outline block class="mt-4" @click="submit">Submit Quiz</v-btn>
        </v-flex>
    </v-layout>
</template>

<script>
export default {
    data() {
        return {
            quiz: {
                quizTitle: '',
                noOfQuestions: '1',
                questions: [],
                options: []
            },
            correct: [],
        }
    },
    created() {
        this.getQuiz()
    },
    methods: {
        convert(val) {
            const arr = [];
            for (let i = 1; i < val + 1; i++) {
                arr[i - 1] = i.toString();
            }
            return arr;
        },
        getQuiz() {
            this.$axios.$post('/api/getQuiz',
            {
                quizLink: this.$route.params.quiz
            }).then(res => {
                if(res.message === 'Error') {
                    this.$notify({
                        group: 'notify',
                        title: 'Wrong Link',
                        text: 'This Quiz link does not exist. Enter a valid link.'
                    })
                    this.$router.push('/home')
                }
                else {
                    this.quiz = res.quiz
                    this.setCorrect(Number(res.quiz.noOfQuestions))
                }
            })
        },
        setCorrect(len) {
            this.correct.length = len;
            for (let i = 0; i < len; i++) {
                if(this.correct[i] === undefined) {
                    const arr = [];
                    this.correct[i] = arr;
                }
            }
        },
        reset(id, index) {
            if(this.correct[index].includes(`Option ${id}`)) {
                const ind = this.correct[index].indexOf(`Option ${id}`)
                if (ind > -1) {
                    this.correct[index].splice(ind, 1)
                }
            }
        },
        submit() {
            if(this.checkCorrect()) {
                this.$axios.$post('/api/evaluateQuiz',
                {
                    quizLink: this.$route.params.quiz,
                    submitted: this.correct
                })
                .then(res => {
                    this.$notify({
                    group: 'notify',
                    title: 'Your Score',
                    text: `Great. You anwered ${res.marks} out of ${res.total} questions correctly.`
                    })
                    this.$router.push('/home')
                })
            }
            else {
                this.$notify({
                    group: 'notify',
                    title: 'Attempt all questions',
                    text: 'Some questions are left. Attempt all to submit your answers.'
                });
            }  
        },
        checkCorrect() {
            for (let i = 0; i < Number(this.quiz.noOfQuestions); i++) {
                if(this.correct[i].length === 0) {
                    return false
                }
            }
            return true
        }
    }
}
</script>