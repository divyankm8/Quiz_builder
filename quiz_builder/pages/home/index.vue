<template>
    <v-container>
        <v-layout>
            <v-flex xs12>
                <v-card>
                    <v-card-text>
                        <v-flex xs12>
                            <v-text-field v-model="link" label="Enter any quiz link to take quiz" type="link" solo single-line></v-text-field>
                            <n-link :to="`/${link}`">
                                <v-btn class="indigo" dark>Take quiz</v-btn>
                            </n-link>
                        </v-flex>
                    </v-card-text>
                </v-card>
                <v-card>
                    <v-card-title>
                        <h1 class="display-1">All Quiz</h1>
                        <v-spacer></v-spacer>
                        <n-link to="/home/create">
                            <v-btn small color="grey darken-2" dark>Create New Quiz</v-btn>
                        </n-link>
                    </v-card-title>
                    <v-card-text>
                        <v-data-table :headers="headers" :items="quizAll" :items-per-page="5" class="elevation-3">
                            <template v-slot:body="{ items }">
                                <tr v-for="item in items" :key="item.quizLink">
                                    <td><n-link :to="`/${item.quizLink}`">{{ item.quizLink }}</n-link></td>
                                    <td>{{ item.quizTitle }}</td>
                                    <td>
                                        <v-icon small @click="destroy(item.quizLink)">delete</v-icon>
                                    </td>
                                </tr>
                            </template>
                        </v-data-table>
                    </v-card-text>
                </v-card>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
import 'material-design-icons-iconfont/dist/material-design-icons.css'
export default {
    middleware: 'auth',
    data() {
        return {
            headers: [
                { text: 'Quiz Link (Click on link to take quiz)', value: 'quizLink' },
                { text: 'Quiz Title', value: 'quizTitle' },
                { text: 'Delete Quiz', value: 'action' }
            ],
            quizAll: [],
            link: ''
        }
    },
    created() {
        this.fetchQuiz()
    },
    methods: {
        fetchQuiz() {
            this.$axios.$post('/api/fetchQuiz',
            {
                email: this.$store.state.auth.emailId
            }).then(res => {
                this.quizAll = res.quiz
            })
        },
        destroy(link) {
            this.$axios.$post('/api/deleteQuiz',
            {
                quizLink: link
            })
            this.quizAll.splice(this.quizAll.indexOf(link), 1)
        },
    }
}
</script>

