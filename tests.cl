; odd and even are defined to test the recursion
(define odd? (lambda (n) 
	(if (= n 0) false
	(even? (- n 1)))))

(define even? (lambda (n)
	(if (= n 0) true
	(odd? (- n 1)))))

; for testing the limits of my recursion and higher order functions
(define only-even (lambda (li) 
	(filter (lambda (n) 
		(even? n)) li)))


; here are some examples of typical lisp code that doesn't work in this language
; this is because when i was coding this i was focused on the parsing and running the eval function
; from the original lisp paper and i didn't consider scope at all so i forgot to properly implement
; either static or dynamic scope, so now nothing works properly and closures "will" not work.
; (define flip (lambda (f) (lambda (a b) (f b a))))
; (define compose (lambda (f1 f2) (lambda (a) (f1 (f2 a)))))
