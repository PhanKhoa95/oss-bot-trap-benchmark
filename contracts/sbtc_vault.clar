;; sBTC 128-bit Vault Share Calculator
(define-constant ERR-ZERO-DENOMINATOR (err u100))
(define-constant ERR-INVALID-FEE-BPS (err u101))
(define-constant BPS-DENOMINATOR u10000)

(define-public (calculate-net-share (amount uint) (fee-bps uint) (total-supply uint))
  (begin
    (asserts! (> total-supply u0) ERR-ZERO-DENOMINATOR)
    (asserts! (<= fee-bps BPS-DENOMINATOR) ERR-INVALID-FEE-BPS)
    (let ((net-amount (/ (* amount (- BPS-DENOMINATOR fee-bps)) BPS-DENOMINATOR)))
      (ok net-amount)
    )
  )
)
