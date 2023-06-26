#ifndef _POLYNFIELD_H_
#define _POLYNFIELD_H_

#include "polyn_arithmetic.h"

namespace polfld{
    class polField{

        private:
            int order; // 2^n
            polyn::Polynomial ** multiplicationTable; // [order] x [order] = size
            int degree; // n
            
            long long int mx; // nth bit represents coefficient of x^n (mod 2)
            // mx must be a prime polynomial or degree n

        public:
            polField(void) {
                order = 0;
                degree = 0;
                multiplicationTable = nullptr;
            }

        private:
            void genMultTable(void) noexcept {

                multiplicationTable = new polyn::Polynomial * [order];

                for (int i = 0; i < order; i ++) {
                    multiplicationTable[i] = new polyn::Polynomial [order];
                    for (int j = 0; j < order; j++){
                        // IMPLEMENT * OPERATOR FIRST!!!!
                        // THEN IMPLEMENT % OPERATOR
                        // THEN FINISH THIS!!
                    }
                }

            }

        public:
            polField(int d, int n, int mx) : degree(d), order( (1 << n) ), mx(mx) {
                genMultTable();
            }

    }; // struct polField


} // namespace polField


#endif