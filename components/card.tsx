import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import { CardActionArea } from '@mui/material';
import { Movie } from '../typings'
import { readdir } from 'fs';
import React, {useState} from 'react';
import axios from 'axios';

interface Props {
  userID: number
  movie: Movie
}


export default function ActionAreaCard({userID,movie }: Props) {
    const [bordcolor,setbordercolor] = useState('#001253')
    const [bordwidth,setborderwidth] = useState(3)
    return (
        <div className='cursor-pointer'
        onClick={() => {
            if(bordcolor=='#001253'){
                setbordercolor('#81C6E8');
                axios({
                    url: "http://localhost:5000/addtomylist",
                    method: 'POST',
                    data: [userID,movie.id]
                  });
            }
            else{
                setbordercolor('#001253')
            }
            if(bordwidth==3){
                setborderwidth(4)
            }
            else{
                setborderwidth(3)
            }

          }}
        >
            
      <Card sx={{ maxWidth: 250, borderWidth:bordwidth,borderColor: bordcolor, borderRadius: 7}}>
        <CardActionArea>
          <CardMedia
            component="img"
            height="80"
            image= {`https://image.tmdb.org/t/p/w500${
                movie.backdrop_path || movie.poster_path
              }`}
            alt="green iguana"
          />
          <CardContent sx={{color: '#508FCD', backgroundColor: 'black',textAlign:'center'}}>
            <Typography gutterBottom variant="subtitle2" component="div">
              {movie.title || movie.original_name}
            </Typography>
            {/* <Typography variant="body2" color="text.secondary">
              {movie.popularity}
            </Typography> */}
          </CardContent>
        </CardActionArea>
      </Card>
      </div>
    );
  }