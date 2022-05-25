const primeNumber = 95971


function modulo(a, m) {
    result = a % m
    return result < 0 ? result + m : result
}


function modInverse(a, m) {
    [a, m] = [Number(a), Number(m)]
    if (Number.isNaN(a) || Number.isNaN(m)) {
        return NaN
    }


    a = (a % m + m) % m
    if (!a || m < 2) {
        return NaN
    }


    const s = []
    let b = m
    while (b) {
        [a, b] = [b, a % b]
        s.push({ a, b })
    }
    if (a !== 1) {
        return NaN
    }


    let x = 1, y = 0
    for (let i = s.length - 2; i >= 0; --i) {
        [x, y] = [y, x - y * Math.floor(s[i].a / s[i].b)]
    }
    return (y % m + m) % m
}


function getRandomInt() {
	return Math.floor((Math.random() * primeNumber) + 1) % primeNumber
}


function IsExistX(shares, N, x, s) {
    for (let i = 0; i < N; i++) {
        if (shares[i][s][0] == x) {
            return true
        }
    }


    return false
}


function create(message, K, N) {
    const messageBuffer = new Buffer.from(message) // 전달 받은 메시지를 Buffer로 변경
    const secrets = [...messageBuffer] // Buffer를 Array형태로 변경
    const polynomial = new Array(K).fill(0) // 다항식 기본 형태 생성
	const shares = new Array(N) // 각 사용자들에게 나눠줄 share(point) 배열 생성
	
	for(let i=0;i<N;i++){ // Array allocation
		shares[i]=new Array(secrets.length)
	}
	
	for (let s = 0; s < secrets.length; s++) { // 하나의 charater에 대해서..
		polynomial[0] = secrets[s] // 비밀키를 다항식의 상수에 저장 
		for (let j = 1; j < K; j++) {
            polynomial[j] = getRandomInt() // 각 차수에 계수를 랜덤하게 추출
        }
		for(let i=0;i<N;i++){
			shares[i][s] = new Array(2)
            do {
                x = getRandomInt();
            } while (IsExistX(shares, i, x, s));
            shares[i][s][0] = x
            shares[i][s][1] = evaludatePolynomial(polynomial, x) // f(x)를 계산하여 y에 대입
		}
	}
	return shares
}


function evaludatePolynomial(polynomial, x) {
    const last = polynomial.length - 1
    let result = polynomial[last]


    for (let i = last - 1; i >= 0; i--) {
        result = result * x
        result = result + polynomial[i]
        result = modulo(result, primeNumber)
    }


    return result
}




function combine(shares) { // 라그랑주 기초 다항식 공식을 활용하여 다항식 계산 및 L(0) 계산
  //let secret = 0

	var buffer = new Buffer.alloc(shares[0].length); //shares[0].length = input의 length와 동일
	
	for (let i = 0; i < shares[0].length; i++) {
    let secret=0
		for(let j=0;j<shares.length;j++){
			const share=shares[j][i] 
			const x = share[0]
			const y = share[1]
			
			let numerator = 1
			let denominator = 1
			for(let k=0;k<shares.length;k++){
				if (j != k) {
                numerator = numerator * -shares[k][i][0]
                numerator = modulo(numerator, primeNumber)
                denominator = denominator * (x - shares[k][i][0])
                denominator = modulo(denominator, primeNumber)
				}
			}
			
			inversed = modInverse(denominator, primeNumber)
			secret = secret + y * (numerator * inversed) // P48. L(X) 공식 계산
			secret = modulo(secret, primeNumber)
			
		}
		buffer[i] = secret
		
	}
  return buffer
}


const shares = create('12j3k2j1l', 5, 10) //shares 3차원배열은 [N][input.length][2]로 구성되어있다.
console.log(combine(shares.slice(1, 6)).toString())

