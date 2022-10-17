const surveyData = {
    int_learn: [
        {
            question: "Blockchain projects development increases my opportunities for a better job."
        },
        {
            question: "I earn respect from others by participating in Blockchain project."
        },
        {
            question: "Participation in Blockchain project improves my reputation in the profession."
        }
    ],
    fin_gain: [
        {
            question: "I am paid in the form of cryptocurrency to work for the Blockchain project."
        },
        {
            question: "I receive some form of compensation in the form of crypto for participating in the Blockchain project."
        },
        {
            question: "For me, working for the Blockchain project is extremely profitable."
        },
        {
            question: "Comparing to other programming jobs, working for the Blockchain project is very poorly paid."
        }
    ],
    expert_hetro: [
        {
            question: "I believe members of the Blockchain project on which I work vary widely in their areas of expertise"
        },
        {
            question: "I believe members of the Blockchain project on which I work have a variety of different backgrounds and experiences"
        },
        {
            question: "I believe members of the Blockchain project on which I work have skills and abilities that complement each other’s"
        }
    ],
    tech_norm: [
        {
            question: "I think that, it is wrong to hard fork a Blockchain project."
        },
        {
            question: "I believe it is inappropriate to distribute Blockchain code changes without going through the proper channels."
        },
        {
            question: "I believe that with enough developers working on a particular Blockchain project, any bug can be quickly found and fixed."
        },
        {
            question: "I place great value on technical knowledge in a Blockchain project."
        },
        {
            question: "I think co-operation in Blockchain community is important."
        }
    ]
    ,
    sys_int: [
        {
            question: "I synthesize and integrate my expertise at the Blockchain implementation level."
        },
        {
            question: "I believe members of the Blockchain project on which I work span several areas of expertise to develop shared Blockchain project concepts."
        },
        {
            question: "I can clearly see how different pieces of Blockchain project fit together."
        },
        {
            question: "I competently blend new Blockchain project-related knowledge with what I have already know."
        }
    ],
    code_test: [
        {
            question: "The more difficult the Blockchain code testing problem, the more I enjoy trying to solve it."
        },
        {
            question: "I enjoy relatively complex, complicated Blockchain software code testing tasks."
        },
        {
            question: "I enjoy tackling Blockchain testing problems that are completely new to me."
        },
        {
            question: "I prefer software testing work I know whether I can do well, over software testing that stretched my abilities."
        },
        {
            question: "I enjoy trying to solve complex Blockchain problems."
        }
    ],
    cont_code_dec: [
        {
            question: "To what extent the relationship between your contributed code and the Blockchain core project was characterized by plug-and-play."
        },
        {
            question: "To what extent the relationship between your contributed code and the Blockchain core project was characterized by highly modular."
        },
        {
            question: "To what extent the relationship between your contributed code and the Blockchain core project was characterized by highly interoperable."
        },
        {
            question: "To what extent the relationship between your contributed code and the Blockchain core project was characterized by loosely coupled."
        },
        {
            question: "To what extent the relationship between your contributed code and the Blockchain core project was characterized by small number of interdependencies."
        }
    ],
    dec_right_del: [
        {
            question: "To what extent the responsibility was distributed between you and the core developers for making decisions about the project features extension."
        },
        {
            question: "To what extent the responsibility was distributed between you and the core developers for making decisions about the functionality extension."
        },
        {
            question: "To what extent the responsibility was distributed between you and the core developers for making decisions about the Design extension."
        },
        {
            question: "To what extent the responsibility was distributed between you and the core developers for making decisions about the implementation extension."
        },
        {
            question: "To what extent the responsibility was distributed between you and the Blockchain community for making decisions about the user interface extension."
        }
    ],
    dev_inv: [
        {
            question: "I consider the Blockchain project to be significant."
        },
        {
            question: "The Blockchain project means a lot to me."
        },
        {
            question: "The Blockchain project is of concern to me."
        },
        {
            question: "I consider the Blockchain project to be relevant to me."
        },
        {
            question: "The Blockchain project matters to me."
        }
    ],
    proj_desertion: [
        {
            question: "How frequently do you desert a Blockchain project after having created code patch for the same project implementation?"
        },
        {
            question: "How often do you leave your created code patch for a Blockchain project without contributing them?"
        },
        {
            question: "How often do you create code patch for a Blockchain project, but do not contribute it to the same project?"
        },
        {
            question: "How often do you close your project user ID, before you contribute the code patches to a Blockchain project?"
        },
        {
            question: "How often do you desert a Blockchain project ?"
        }
    ],
    dev_experience: [
        {
            question: "How many years of experience do have in Blockchain Technology ?"
        }
    ]
}

// get the keys of the surveyData -> quiz cats
const quizKeys = Object.keys(surveyData) //["int_learn","fin_gain"...]
const categories = {
    int_learn: "Intention to Learn",
    fin_gain: "Financial Gain",
    expert_hetro: "Expert Hetrogenity",
    tech_norm: "Technical Norm",
    sys_int: "System Integration",
    code_test: "Code Testing Task",
    cont_code_dec: "Continuous Code Integration",
    dec_right_del: "Decision Right Delegation",
    dev_inv: "Developer Involvement",
    proj_desertion: "Project Desertion",
    dev_experience: "Developer Experience"
}

// The response object
const responseObj = {
    int_learn: '',
    fin_gain: '',
    tech_norm: '',
    sys_int: '',
    code_test: '',
    cont_code_dec: '',
    dec_right_del: '',
    dev_inv: '',
    proj_desertion: '',
    dev_experience: ''
}


// elements
const quiz = document.getElementById('quiz')
const answerEls = document.querySelectorAll('.answer')
const questionEl = document.getElementById('question')
const submitBtn = document.getElementById('submit')
const errorElem = document.getElementById('error')
const qcatElem = document.getElementById('qcat')
const qcounterElem = document.getElementById('qcounter')

//get the total number of questions
let totalQs = 0
let currentCounter = 1;
for(let i = 0; i < quizKeys.length; i++){
    let cCat = surveyData[quizKeys[i]];
    totalQs += cCat.length
}
qcounterElem.innerHTML = `${currentCounter} of ${totalQs}`
//quiz cat index -> starting point
let currentKey = 0

//quiz current category
let currentCat = surveyData[quizKeys[currentKey]]

let currentCatText = quizKeys[currentKey]

qcatElem.innerHTML = `${categories[currentCatText]}`
//current quiz question
let currentQuiz = 0

//load the quiz
loadQuiz()


// A function to load the quiz
function loadQuiz() {
    // deselect an answer when the next question is loaded
    deselectAnswers()

    const currentsurveyData = currentCat[currentQuiz]


    questionEl.innerText = currentsurveyData.question
    
}

// A function to deselect an answer elemennt
function deselectAnswers() {
    answerEls.forEach(answerEl => answerEl.checked = false)
}

function getSelected() {
    let answer

    answerEls.forEach(answerEl => {
        if(answerEl.checked) {
            answer = answerEl.id
        }
    })

    return answer
}

submitBtn.addEventListener('click', () => {
    
    //update the dom for dev_exp
    if(currentCounter === totalQs-1){
        // hide the seventh element
        document.getElementById('seven').style.display = 'none'
        //change the elements to display years
        document.getElementById('one').innerHTML = '1 year'
        document.getElementById('two').innerHTML = '2 years'
        document.getElementById('three').innerHTML = '3 years'
        document.getElementById('four').innerHTML = '4 years'
        document.getElementById('five').innerHTML = '5 years'
        document.getElementById('six').innerHTML = '6 years'
    }
    

    //get the selected answer
    const answer = getSelected()

    //set error elem display to none
    errorElem.style.display = 'none';

    //if question is answered get the next question
    if(answer != undefined /*|| answer == undefined*/){

        //the current question
        const currentsurveyData = currentCat[currentQuiz]

        //set the answer to a particular question by updating the obj
        currentsurveyData['answer'] = answer
        
        //update counter & the element
        currentCounter++;
        qcounterElem.innerHTML = `${currentCounter} of ${totalQs}`;

        // go to the next question
        currentQuiz++;

        if(currentQuiz < currentCat.length) {
            loadQuiz()
        }
        else
        {
            // calculate the average of last cat and push it to responseObj
            // currentCat is an array of questions objs

            let sum = 0;
            for(let q = 0; q < currentCat.length; q++){
                sum = sum + Number(currentCat[q]['answer'])
            }
            //update responseObj to be the avg of the current cat
            let catKey = quizKeys[currentKey]
            if(catKey !== 'expert_hetro'){
                responseObj[catKey] = Number((sum/currentCat.length).toFixed(2));
            }
            //increment the category current key to the next cat
            currentKey++;
            // set currentCatText to next
            currentCatText = quizKeys[currentKey]
            //update the DOM
            qcatElem.innerHTML = `${categories[currentCatText]}`

            //reset currentQuiz
            if(currentKey < quizKeys.length){
                currentQuiz = 0

                //set current cat to next cat
                currentCat = surveyData[quizKeys[currentKey]]
                loadQuiz()
            }
            else
            {
                //last cat
                if(currentQuiz === currentCat.length){
                    //do something
                    let form = `
                    <form>
                        <h4 style="text-align: center;">Enter your Name & Email Address</h4>
                        <br/>
                        <center><small style="font-size: 18px; font-weight:bold;" id="formsuccess"></small></center>
                        <br/>
                        <div class="row">
                            <div class="col-md-6" style="margin: 0 auto;">
                                <div class="form-floating mb-3">
                                    <input class="form-control" id="name" name="name" type="text" placeholder="Enter your name..." required />
                                    <label for="name">Full name</label>
                                    <div class="invalid-feedback" data-sb-feedback="name:required">A name is required.</div>
                                </div>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-6" style="margin: 0 auto;">
                                <div class="form-floating mb-3">
                                    <input class="form-control" id="email" name="email" type="email" placeholder="Email Address..." required />
                                    <label for="email">Email</label>
                                    <div class="invalid-feedback" data-sb-feedback="name:required">Email.</div>
                                </div>
                            </div>
                        </div>
                        <div class='row'>
                            <div class="col-md-6" style="margin: 0 auto;">
                                <div class="form-floating mb-3">
                                    <select id="education" name="education" class="form-control" required>
                                        <option value=""></option>
                                        <option value="doctorate">Doctorate</option>
                                        <option value="master">Master</option>
                                        <option value="bachelor">Bachelor</option>
                                        <option value="high">High School</option>
                                    </select>
                                    <label for="education"><b>Select Education</b></label>
                                </div>
                            </div>
                        </div>
                        
                        <div class='row'>
                            <div class="col-md-6" style="margin: 0 auto;">
                                <div class="form-floating mb-3">
                                    <select id="region" name="region" class="form-control" required>
                                        <option value=""></option>
                                        <option value="asia">Asia</option>
                                        <option value="caribbean">Caribbean</option>
                                        <option value="central america">Central America</option>
                                        <option value="oceania">Oceania</option>
                                        <option value="europe">Europe</option>
                                        <option value="north america">North America</option>
                                        <option value="south america">South America</option>
                                    </select>
                                    <label for="region"><b>Select Region</b></label>
                                </div>
                            </div>
                        </div>

                        <div class='row'>
                            <div class="col-md-6" style="margin: 0 auto;">
                                <div class="form-floating mb-3">
                                    <select class="form-control" name="proj_age" id="proj_age" required>
                                        <option value=""></option>
                                        <option value="1">1 month</option>
                                        <option value="2">2 months</option>
                                        <option value="3">3 months</option>
                                        <option value="4">4 months</option>
                                        <option value="5">5 months</option>
                                        <option value="6">6 months</option>
                                    </select>
                                    <label for="dev_status"><b>Current Project Age</b></label>
                                </div>
                            </div>
                        </div>
                        <center><small style="color: red; display: none; font-size: 15px;" id="formerror">All fields the are required!</small></center>
                        <div class="row gx-4 gx-lg-5 justify-content-center mt-2 mb-5">
                            <div class="col-lg-6">
                                <div class="d-grid"><button class="btn btn-success btn-xl" id="submitButton" type="submit">Submit</button></div>
                            </div>
                        </div>
                    </form>
                    `
                    document.getElementById('details-form').innerHTML = form

                    // details elements
                    const nameElem = document.getElementById('name')
                    const emailElem = document.getElementById('email')
                    const educationElem = document.getElementById('education')
                    const regionElem = document.getElementById('region')
                    const proj_ageElem = document.getElementById('proj_age')
                    const submitBtnDetails = document.getElementById('submitButton')

                    submitBtnDetails.addEventListener('click', function(event){
                        event.preventDefault();

                        if(document.querySelector('form').checkValidity()){
                            // add the values to responseObj
                            responseObj['name'] = nameElem.value
                            responseObj['email'] = emailElem.value
                            responseObj['education'] = educationElem.value
                            responseObj['region'] = regionElem.value
                            responseObj['proj_age'] = proj_ageElem.value

                            $.ajax({
                              url:"/",
                              method:"POST",
                              data: responseObj,
                              success: function(res){

                                let successElem = document.getElementById('formsuccess');
                                if(res.success === true){
                                    successElem.style.color = 'green'
                                    successElem.innerHTML = 'You\'ve Successfully submitted your data.'                                
                                }
                                else{
                                    successElem.style.color = 'red'
                                    successElem.innerHTML = 'You\'ve Already submitted your data.'                                
                                }
                                window.location.href = res.redirect
                              },
                              error: function(xhr, status, error){
                                console.log(error)
                              }
                                  
                             });

                        }
                        else
                        {
                            document.getElementById('formerror').style.display = 'block'
                            setTimeout(function(){
                                document.getElementById('formerror').style.display = 'none'
                            }, 3000)
                        }
                    })

                }
            }
        }
    }
    else
    {
        errorElem.style.display = 'block';
    }

})