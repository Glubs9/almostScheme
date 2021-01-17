; macros
(define if (lambda-macro (p a b) (cond ((eval p) (eval a)) (true (eval b)))))
; very clever definition of apply
(define apply (lambda-macro (f li) (eval (cons f li)))) 


; number functions
(define max (lambda (n1 n2) (if (> n1 n2) n1 n2)))
(define min (lambda (n1 n2) (if (< n1 n2) n1 n2)))
(define abs (lambda (n) (if (> 0 n) n (* n -1))))

; probably define all the rounding functions here

; doesn't work?
(define pow (lambda (base, expo)
	(if (= expo 0) 1 
	(* base (pow base (- expo 1))))))


; list functions
(define join (lambda (li1 li2) (+ li1 li2)))
; note: join *should* be defined recursively but this is more efficient

(define reduce (lambda (f li start)
	(if (empty li) (eval start)
	(f (car li) (reduce f (cdr li) start)))))

(define map (lambda (func li)
	(if (empty li) li
	(cons (func (car li)) (map func (cdr li))))))

(define bind (lambda (f li)
	(if (empty li) li
	(join (f (car li)) (bind f (cdr li))))))

(define filter (lambda (f li)
	(if (empty li) e
	(let ((head (car li)) (next (filter f (cdr li))))
	(if (f head) (cons head next) next)))))

(define and-list (lambda (li) (reduce and li true)))
(define or-list (lambda (li) (reduce or li true)))
(define sum (lambda (li) (reduce + li 0)))
(define product (lambda (li) (reduce * li 1)))
(define maximum (lambda (li) (reduce max li -999999)))
(define minimum (lambda (li) (reduce min li 999999)))

(define print-list (lambda (li) (begin (map (lambda (n) (begin
	(dispnnl n)
	(dispchar 44)
	(dispchar 32)
)) li) (dispchar 10))))

(define length (lambda (li) (sum (map (lambda (n) 1) li))))

; extended cars and cdrs
(define caar (lambda (n) (car (car n))))
(define cadr (lambda (n) (cdr (car n))))
(define cdar (lambda (n) (car (cdr n))))
(define cddr (lambda (n) (cdr (cdr n))))

(define range (lambda (low high) 
	(if (= low high) e
	(cons low (range (+ 1 low) high)))))

(define drop (lambda (n li)
	(if (= 0 n) li
	(drop (- n 1) (cdr li)))))
(define take (lambda (n li)
	(if (= 0 n) e
	(cons (car li) (take (- n 1) (cdr li))))))
(define slice (lambda (start end li)
	(take (- end start) (drop (- start 1) li))))

; maybe redefine with cond
(define in (lambda (v li) 
	(if (empty li) false
	(if (= (car li) v) true
	(in v (cdr li))))))

(define zip (lambda (li1 li2)
	(if (or (empty li1) (empty li2)) e
	(cons (list (car li1) (car li2))
		(zip (cdr li1) (cdr li2))))))

(define delete (lambda (v li)
	(if (empty li) e
	(if (= v (car li)) (cdr li)
	(cons (car li) (delete v (cdr li)))))))

; reverse is a bit slow
(define reverse (lambda (li)
	(if (empty li) li
	(cons (last li) (reverse (init li))))))


; sorting functions below
; these are more to demonstrate the power of the language rather than practicality
(define select-sort (lambda (li)
	(if (empty li) li
	(let ((smallest (minimum li)))
	(cons smallest (select-sort (delete smallest li)))))))
