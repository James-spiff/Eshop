import React from 'react'


//This uses star icons to reps the ratings gives a full star for a full rating and a half star for a half rating. There are 5 stars for every product 
function Rating({ value, text, color }) {
    return (
        <div className="rating">
            <span>
                <i style={{ color }} className={
                    value >= 1
                    ? 'fas fa-star'
                    : value >=0.5
                        ? 'fas fa-star-half-alt'
                        : 'far fa-star'
                }>

                </i>
            </span>

            <span>
                <i style={{ color }} className={
                    value >= 2
                    ? 'fas fa-star'
                    : value >=1.5
                        ? 'fas fa-star-half-alt'
                        : 'far fa-star'
                }>

                </i>
            </span>

            <span>
                <i style={{ color }} className={
                    value >= 3
                    ? 'fas fa-star'
                    : value >=2.5
                        ? 'fas fa-star-half-alt'
                        : 'far fa-star'
                }>

                </i>
            </span>

            <span>
                <i style={{ color }} className={
                    value >= 4
                    ? 'fas fa-star'
                    : value >=3.5
                        ? 'fas fa-star-half-alt'
                        : 'far fa-star'
                }>

                </i>
            </span>

            <span>
                <i style={{ color }} className={
                    value >= 5
                    ? 'fas fa-star'
                    : value >=4.5
                        ? 'fas fa-star-half-alt'
                        : 'far fa-star'
                }>

                </i>
            </span>

            <span>
                { text && text }
            </span>
        </div>
    )
}

export default Rating
