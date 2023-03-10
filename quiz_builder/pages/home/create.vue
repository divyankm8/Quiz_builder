<template>
    <v-container>
        <v-layout>
            <v-flex xs12>
                <v-card>
                    <v-card-title>
                        <h1 class="display-2">Create New Quiz</h1>
                        <v-spacer></v-spacer>
                        <n-link to="/home">
                            <v-btn small color="grey darken-2" dark>Home</v-btn>
                        </n-link>
                    </v-card-title>
                    <v-card-text>
                        <form @submit.prevent="store">
                            <v-text-field label="Quiz Title" solo v-model="quizTitle"></v-text-field>
                            <v-row justify="center">
                                <v-col sm="6">
                                    <v-select label="Number of Questions" :items="arrayQues" v-model="numbers.questions"></v-select>
                                    <p>Remove Selected Options by Right Click</p>
                                </v-col>
                            </v-row>
                            <v-card v-for="(questionId, index1) in convert(numbers.questions)" :key="index1">
                                <v-card-title>
                                    <h1 class="display-1">Question {{ questionId }}</h1>
                                </v-card-title>
                                <v-card-text>
                                    <v-text-field label="Question" solo v-model="questions[index1]"></v-text-field>
                                    <v-row justify="center">
                                        <v-col sm="6"><v-select label="Number of Options" :items="arrayOption" v-model="numbers.options[index1]"></v-select></v-col>
                                    </v-row>
                                    <v-text-field v-for="(optionId, index2) in convertOptions(numbers.options[index1])" :key="index2" :label="'Option ' + optionId" solo v-model="options[index1][index2]"></v-text-field>
                                    <v-radio-group row v-model="correct[index1]" multiple>
                                        <p class="mr-4">Choose Correct Answer</p>
                                        <v-radio v-for="(correctId, index3) in convert(numbers.options[index1])" :key="index3" :value="'Option ' + correctId" :label="'Option ' + correctId" @mouseup="reset(correctId, index1)" class="ml-4"></v-radio>
                                    </v-radio-group>
                                </v-card-text>
                            </v-card>
                            <v-btn class="indigo" block dark type="submit">Add Quiz</v-btn>
                        </form>
                    </v-card-text>
                </v-card>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
export default{
    data() {
        return{
            quizTitle: '',
            questions: [],
            options: [],
            correct: [],
            numbers: {
                questions: '1',
                options: []
            },
            arrayQues: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
            arrayOption: ['2', '3', '4', '5'],
        }
    },
    computed: {
        setArrays() {
            this.questions = this.arrayTrim1(this.questions, Number(this.numbers.questions), '')
            this.options = this.arrayTrim2(this.options, Number(this.numbers.questions))
            this.correct = this.arrayTrim2(this.correct, Number(this.numbers.questions))
            this.numbers.options = this.arrayTrim1(this.numbers.options, Number(this.numbers.questions), '2')
            for (let i = 0; i < Number(this.numbers.questions); i++) {
                this.options[i] = this.arrayTrim1(this.options[i], Number(this.numbers.options[i]), '')
            }
        }
    },
    methods: {
        convert(str) {
            const arr = [];
            for (let i = 1; i < Number(str) + 1; i++) {
                arr[i - 1] = i.toString();
            }
            return arr;
        },
        convertOptions(str) {
            this.options = this.arrayTrim2(this.options, Number(this.numbers.questions))
            this.correct = this.arrayTrim2(this.correct, Number(this.numbers.questions))
            return this.convert(str)
        },
        arrayTrim1(array, len, value) {
            array.length = len;
            for (let i = 0; i < len; i++) {
                if(array[i] === undefined) {
                    array[i] = value;
                }
            }
            return array;
        },
        arrayTrim2(array, len) {
            array.length = len;
            for (let i = 0; i < len; i++) {
                if(array[i] === undefined) {
                    const arr = [];
                    array[i] = arr;
                }
            }
            return array;
        },
        reset(id, index) {
            if(this.correct[index].includes(`Option ${id}`)) {
                const ind = this.correct[index].indexOf(`Option ${id}`)
                if (ind > -1) {
                    this.correct[index].splice(ind, 1)
                }
            }
        },
        checkArray() {
            if(this.quizTitle === '') {
                return false
            }
            for (let i = 0; i < Number(this.numbers.questions); i++) {
                if(this.questions[i] === '' || this.correct[i].length === 0) {
                    return false
                }
                for (let j = 0; j < this.options[i].length; j++) {
                    if(this.options[i][j] === '') {
                        return false
                    }
                }
            }
            return true
        },
        store() {
            if(this.checkArray()) {
                this.$axios.$post('/api/createQuiz',
                {
                    userId: this.$store.state.auth.emailId,
                    quizTitle: this.quizTitle,
                    noOfQuestions: Number(this.numbers.questions),
                    questions: this.questions,
                    options: this.options,
                    correct: this.correct
                })
                .then(res => {
                    this.$notify({
                    group: 'notify',
                    title: 'Hooray!! New Quiz Added',
                    text: `New quiz link is => ${res.link}. Share with your friends.`
                    })
                    this.$router.push('/home')
                })
            }
            else {
                this.$notify({
                    group: 'notify',
                    title: 'Fill all fields',
                    text: 'Some fields are left unfilled. Fill all to add your quiz.'
                });
            }
        }
    }
}
</script>