pipeline {
    agent any // נותן לג'נקינס גמישות להתחיל, אבל הסטייג'ים יקבעו איפה לרוץ

    environment {
        PYTHONIOENCODING = 'utf-8'
    }

    parameters {
        // --- הכפתור החדש לבחירת המכונה ---
        choice(name: 'EXECUTOR_NODE', choices: ['windows', 'linux'], description: 'Select the machine to run on')
        
        // שאר הפרמטרים של המשחק
        string(name: 'PLAYER_NAME', defaultValue: 'Eliad', description: 'Name of the Hero')
        choice(name: 'HERO_CLASS', choices: ['Warrior', 'Mage', 'Rogue'], description: 'Choose your class')
        string(name: 'LEVEL', defaultValue: '10', description: 'Hero Level (1-100)')
        booleanParam(name: 'HARDCORE_MODE', defaultValue: false, description: 'Enable Hardcore Mode?')
    }

    stages {
        stage('Game Execution') {
            // כאן הקסם קורה: ג'נקינס יבחר מכונה לפי מה שסימנת בתפריט
            agent { label "${params.EXECUTOR_NODE}" }
            
            steps {
                // בדיקה: הדפסה על איזה מחשב אנחנו רצים
                echo "Running on node: ${env.NODE_NAME}"
                
                // שלב 1: משיכת הקוד
                checkout scm
                
                // שלב 2: התקנה (מותאם גם לווינדוס וגם ללינוקס)
                script {
                    if (isUnix()) {
                        sh 'pip install -r requirements.txt --break-system-packages || pip install -r requirements.txt'
                    } else {
                        bat 'python -m pip install -r requirements.txt'
                    }
                }

                // שלב 3: הרצת המשחק
                script {
                    def date = new Date().format("yyyy-MM-dd")
                    echo "Starting battle..."
                    
                    if (isUnix()) {
                        // פקודה ללינוקס
                        sh "python3 dungeon_sim.py --player_name \"${params.PLAYER_NAME}\" --hero_class \"${params.HERO_CLASS}\" --level ${params.LEVEL} --battle_date \"${date}\""
                    } else {
                        // פקודה לווינדוס
                        bat "python dungeon_sim.py --player_name \"${params.PLAYER_NAME}\" --hero_class \"${params.HERO_CLASS}\" --level ${params.LEVEL} --battle_date \"${date}\""
                    }
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '*.html, *.txt', allowEmptyArchive: true
        }
    }
}
