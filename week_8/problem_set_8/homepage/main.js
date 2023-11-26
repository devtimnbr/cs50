// add footer to each page
const footer = document.createElement('footer')
const a = document.createElement('a')
a.href = 'https://timneubauer.dev'
a.target = '_blank'
a.innerText = 'Created by Tim Neubauer'
footer.append(a)
document.querySelector('body').appendChild(footer)
