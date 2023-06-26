#ifndef _POLYN_ARITHMETIC_H_
#define _POLYN_ARITHMETIC_H_

#include <string>
#include <iostream>
#include <iomanip>
#include <sstream>

#define NODEBUG // toggle debug outputs into cout


namespace polyn{

    using namespace std;


    class Polynomial{
        unsigned char * bits;
        unsigned char numBits; // n
        const unsigned char prime = 2; // p


        private:
        void clear(void) noexcept {

            if (!numBits || bits == nullptr){return;}

            for (int i = 0; i < ( (numBits / 8) + ((numBits & 7 == 0) ? (0) : (1) ) ); i++ ){
                bits[i] = 0;
            }

        }
        public: // DO NOT REMOVE

        // FOR SOME REASON DESTRUCTOR DOES NOT WORK??!!!
        // ~Polynomial(){   
        //     if (bits != nullptr)
        //         delete [] bits;
        // }

        Polynomial(void) {
            bits = nullptr;
            numBits = 0;
        }

        Polynomial(char numBits) : numBits(numBits){
            bits = new unsigned char[ (numBits / 8) + ( (numBits & 7 == 0) ? (0) : (1) ) ];
            clear();
        }

        /**
         * @brief indexes according to bit position: lsb = index 0; msb = index length() - 1
         * @return returns a 1 (number not ascii etc. char) or 0 (number not ascii etc. char) 
        */
        unsigned char operator[](const int & index) const {

            if (index >= numBits){
                std::cerr << "Index cannot exceed the total number of bits." << endl;
                throw index; // uncaught
            }
            else {
                const unsigned char mask = 1 << (index % 8);
                return ( (bits[index / 8] & mask) >> (index % 8) );
            }
        }

        private: 
        /**
         * IMPORTANT: does not do any null checks, make sure bits is initalized
        */
        unsigned char & getByteReference(const unsigned int & location){
            return ( bits[location / 8] );
        }
        public: // prev function is private -- DO NOT REMOVE




        /**
         * @brief deep copy constructor
        */
        Polynomial & operator=(const Polynomial & rhs) noexcept {

            if (bits != nullptr){
                delete this->bits;
            }
            this->bits = new unsigned char[rhs.numBits];
            this->numBits = rhs.numBits;

            for (int i = 0; i < this->numBits; i++){
                this->bits[i] = rhs.bits[i];
            }

            this->clear();

            return *this;
        }

        /**
         * @brief Converts string to Polynomial object. 
         * IMPORTANT: Assigns the leftmost bit to the msb and the last bit to the lsb, the rest of the bits follow the same order.
         *            Assigns the first byte to the left to the highest index in the bits array and so forth
        */
        Polynomial & operator=(const string & rhs){

            if (bits != nullptr){
                delete this->bits;
            }
            this->bits = new unsigned char[rhs.length() / 8 + 1];

            this->numBits = rhs.length();

            for (int i = 0; i < (rhs.length() / 8) + 1; i++){
                bits[i] = 0;
            }

            unsigned char mask = 1;

            for (int i = rhs.length() - 1; i >= 0; i--){

                unsigned int bitIndex =  (rhs.length() - i - 1) / 8;

                if (rhs[i] == '1'){
                    bits[ bitIndex] |= mask;
                }
                else if (rhs[i] == '0'){
                    bits[bitIndex] &= ~mask;
                }
                else  {
                    std::cerr << "Nonbinary character in bitstring"<< endl;
                    throw i; // uncaught
                }

                mask = mask << 1;

                if (mask == 0){
                    mask = 1;
                }

            }

            return *this;

        }

        Polynomial(const string & rhs){
            this->bits = new unsigned char[rhs.length() / 8 + 1];

            this->numBits = rhs.length();

            for (int i = 0; i < (rhs.length() / 8) + 1; i++){
                bits[i] = 0;
            }

            unsigned char mask = 1;

            for (int i = rhs.length() - 1; i >= 0; i--){

                unsigned int bitIndex =  (rhs.length() - i - 1) / 8;

                if (rhs[i] == '1'){
                    bits[ bitIndex] |= mask;
                }
                else if (rhs[i] == '0'){
                    bits[bitIndex] &= ~mask;
                }
                else  {
                    std::cerr << "Nonbinary character in bitstring"<< endl;
                    throw i; // uncaught
                }

                mask = mask << 1;

                if (mask == 0){
                    mask = 1;
                }

            }
        }

        /**
         * @brief converts polynomial to string. 
         * IMPORTANT: highest index in the bits array = most significant byte
         * IMPORTANT: highest indexed bit within a byte = most significant bit
        */
        operator std::string () const noexcept {

            string result = "";

            const unsigned int lenArray = (numBits / 8) + ( (numBits % 8 == 0) ? (0) : (1) );
            unsigned int extranBits = (numBits % 8); // extraneous bits
            int shAmount = ( (extranBits == 0) ? (8) : (extranBits) - 1);
        
            for (int i = lenArray - 1; i >= 0; i--){ // i indexes the bits array --> from msb to lsb
                int mask = 1 << shAmount; // how many bits we have in the msb array char
                for (; shAmount >= 0 ;){
                    if (bits[i] & mask){
                        result += '1';
                    }
                    else {
                        result += '0';
                    }

                    if (shAmount >= 0){
                        mask = 1 << --shAmount;
                    }
                }

                shAmount = 7;

            }

            return result;

        }

        operator unsigned long long int() const noexcept {
            unsigned long long int result = 0;

            for ( int i = 0; i < (numBits / 8) + ( (numBits & 7 == 0) ? (0) : (1) ); i++ ){
                result |= ( (bits[i]) << (8 * i) );
            }

            return result;

        }



        friend Polynomial operator* (const Polynomial & lhs, const Polynomial & rhs) noexcept;
        friend Polynomial operator+ (const Polynomial & lhs, const Polynomial & rhs) noexcept;

    }; // struct

    ostream & operator<<(ostream & stream, const Polynomial & rhs) noexcept {
        stream << (string) (rhs);
        return stream;
    }    

    /**
     * @brief addition mod 2 per coefficient in polynomial.
     * Resulting polynomial length = max(length(lhs), length(rhs))
    */
    Polynomial operator+(const Polynomial & lhs, const Polynomial & rhs) noexcept {

        Polynomial result = ( (lhs.numBits >= rhs.numBits) ? (lhs) : (rhs) );

        if (lhs.numBits >= rhs.numBits){
            for (int i = 0; i < (rhs.numBits / 8) + ( (rhs.numBits & 7 == 0) ? (0) : (1) ); i++){
                result.bits[i] ^= rhs.bits[i];
            }

        }
        else {
            for (int i = 0; i < (lhs.numBits / 8) +  ( (rhs.numBits & 7 == 0) ? (0) : (1) ); i++) {
                result.bits[i] ^= lhs.bits[i];
            }

        }

        return result;

    } 

    /**
     * @brief Polynomial multiplication with each coefficient mod 2
    */
    Polynomial operator* (const Polynomial & lhs, const Polynomial & rhs) noexcept {
        unsigned char numBitsResult = lhs.numBits + rhs.numBits; // degree result = degree rhs + degree lhs
        polyn::Polynomial result(numBitsResult);

        for (int i = 0; i < lhs.numBits; i++){ // complexity O(total # of bits in lhs & rhs)
            for (int j = 0; j < rhs.numBits; j++){
                if (lhs[i] == 1 && rhs[j] == 1){
                    result.getByteReference(i + j) ^= (1 << ( (i + j) & 7 ) );
                }
            }
        }

        return result;
    } 

    /**
     * IMPORTANT: currently only supports up to 64 bit sized operands
    */
    Polynomial operator% (const Polynomial & lhs, const Polynomial & rhs) {

        // divisor: rhs, dividend: lhs


        


    }




} // namespace polyn

#endif