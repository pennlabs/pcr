import React from 'react'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'

export default Component => props => (
  <>
    <Navbar />
    <Component {...props} />
    <Footer />
  </>
)
