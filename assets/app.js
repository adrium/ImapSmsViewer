var app = {}

app.baseurl = '/api'

app.vue = new Vue({
	el: '#app',
	data: {
		page: 'numbers',
		id: 'none',
		numbers: [],
		messages: [],
	},
	methods: {
		showNumbers() {
			this.page = 'numbers'
			this.messages = []
			fetch(`${app.baseurl}/numbers`)
				.then(x => x.json()).then(x => this.numbers = x)
		},
		showMessages(id) {
			this.id = id
			this.reloadMessages().then(fn => {
				this.page = 'messages'
			})
		},
		reloadMessages() {
			return fetch(`${app.baseurl}/messages/${this.id}`, { cache: 'no-store' })
				.then(x => x.json()).then(x => this.messages = x)
		}
	},
	mounted() {
		this.showNumbers()
	}
})
