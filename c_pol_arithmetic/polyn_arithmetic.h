#ifndef _POLYN_ARITHMETIC_H_
#define _POLYN_ARITHMETIC_H_

#include <string>
#include <iostream>
#include <iomanip>
#include <sstream>

using namespace std;

#define prdebug(x, debug) if (debug) { cout << (int) (x) << endl; }

#define EDEBUG 1 // toggle debug outputs into cout

namespace pol{

    using namespace std;

    typedef unsigned long long int uint64;
    typedef unsigned long int uint32;
    typedef unsigned char byte;
    typedef unsigned char uint8;
    typedef unsigned short uint16;

    /**
     * IMPORTANT: in its current state only supports polynomials up to x^63 = 64 bits
     * @brief: polynomial arithmetic wrapper with p = 2, 0 < n < 64 
    */
    struct Polynomial{

        uint64 bits;
        uint8 numBits;
        
        Polynomial(void) : bits(0), numBits(0) {}

        Polynomial(uint64 rhs) : bits(rhs) {
            uint8 check = 0;
            while( (1 << check) <= rhs ){
                check++;
            }
            numBits = check;
        }

        /**
         * @brief: string must be in binary formatting without any whitespaces etc. 
        */
        Polynomial(const char * rhs) : Polynomial(strtoull(rhs, nullptr, 2))  {
            prdebug(bits, EDEBUG);
        }

        operator string() const noexcept {
            char temp[33]; // must at least be of size 33 for base 2 (according to docs: ulltoa)
            return ulltoa(bits, temp, 2);
        }

        operator uint64() const noexcept {
            return bits;
        }

        /**
         * @brief return -1 if index > numBits
        */
        signed int operator[](int index) const noexcept {
            if (index > numBits){
                return -1;
            }
            else {
                return ( ( bits & (1 << index) ) >> index );
            }
        }

        friend Polynomial operator+(const Polynomial & lhs, const Polynomial & rhs) noexcept;
        friend Polynomial operator*(const Polynomial & lhs, const Polynomial & rhs) noexcept;
        friend Polynomial operator%(const Polynomial & lhs, const Polynomial & rhs) noexcept;


        private:
            /**
             * @brief: does not do position vs numBits checking
            */
            void inline stclBitAt(const byte & newVal, const byte & position) noexcept {
                if (newVal){ // set
                    bits |= ( 1 << position );
                }
                else { // clr
                    unsigned long long int max = 0;
                    max -= 1; 
                    max ^= ( 1 << position );
                    bits &= max;
                }
            }

        public:


    }; // STRUCT


    Polynomial operator+(const Polynomial & lhs, const Polynomial & rhs) noexcept {
        return (Polynomial) ( lhs.bits ^ rhs.bits );
    }

    Polynomial operator*(const Polynomial & lhs, const Polynomial & rhs) noexcept {
        
        Polynomial result;

        for (int i = 0; i < lhs.numBits; i++){ // complexity O(numBits in lhs + numBits in rhs) = O(num bits in result)
            for (int j = 0; j < rhs.numBits; j++){
                // cout << "lhs[i]: " << lhs[i] << " " << "rhs[j]: " << rhs[j] << endl;
                if (lhs[i] == 1 && rhs[j] == 1){
                    result.bits ^= (1 << (i + j));
                }
            }
        }
        return result;
    }

    Polynomial operator%(const Polynomial & lhs, const Polynomial & rhs) noexcept {
        
    }
} // NAMESPACE

#endif