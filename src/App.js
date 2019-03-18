import React, { Component } from 'react';
import './App.css';
import {Icon, Input, Segment, Grid, Divider, Header, Rating, Button, Loader} from 'semantic-ui-react';
import ReactMarkdown from 'react-markdown';
import io from 'socket.io-client';

const styles = {
    layout: {
        display: "flex",
        flexDirection: 'row',
        flexWrap: "wrap",
        justifyContent: "space-around",
        width: '70vw',
        alignItems: 'center'
    },
    bar: {
        width: '85%'
    }
};

class App extends Component {
    componentWillMount(){
        this.setState({
            loading: false,
            loaded: false,
            error: false,
            level: 0,
            URL: '',
            socket: io.connect('http://localhost:5000/normal', )
        });
    }
    onSubmit(){
        const {socket} = this.state;
        const {googleDatabase, amazonDatabase, whois, phishing, ssl, lastCheck, availableRate, frequent, total, collected} = this.state;

        socket.on('google', (data)=>{this.setState({googleDatabase: data})});
        socket.on('amazon', (data)=>{this.setState({amazonDatabase: data})});
        socket.on('whois', (data)=>{this.setState({whois: data})});
        socket.on('phishing', (data)=>{this.setState({phishing: data})});
        socket.on('ssl', (data)=>{this.setState({ssl: data})});
        socket.on('lastCheck', (data)=>{this.setState({lastCheck: data})});
        socket.on('availableRate', (data)=>{this.setState({availableRate: data})});
        socket.on('frequent', (data)=>{this.setState({frequent: data})});
        socket.on('total', (data)=>{this.setState({total: data})});
        socket.on('collected', (data)=>{this.setState({collected: data})});
        socket.on('loaded', ()=>{this.setState({loading: false})});
        socket.on('level', (data)=>{this.setState({level: data})});
        socket.on('rating', (data)=>{this.setState({rating: data})});

        socket.on('invalid', ()=>{
            this.setState({
                loading: false,
                loaded: false,
                error: true,
            });
        });


        if (this.state.URL === '') {
            this.setState({error: true});
            return
        }
        socket.emit('query', this.state.URL);
        this.setState({error: false, loading: true, loaded: true, googleDatabase: false, amazonDatabase: false,
            whois: false,
            phishing: false,
            ssl: false,
            lastCheck: false,
            availableRate: false,
            frequent: false,
            total: false,
            collected: false,
            level: 0,
            rating: 0
        });
    }
    onRate(e, {rating, maxRating}){
        this.state.socket.emit("rate", {url: this.state.URL, rate: rating});
        this.setState({rating: rating})
    };
    getLevel = (level) => {
        switch (level){
            case 0:
                return (<div style={{
                    color: 'gray',
                    fontSize: '25px',
                    fontWeight: '1000'
                }}>
                    <span className='lds-hourglass' style={{ height: "32px", width: "32px", transform: "translateY(9px)" }}/>
                    Loading
                </div>);
            case 1:
                return (<div style={{
                    color: 'green',
                    fontSize: '25px',
                    fontWeight: '1000'
                }}>
                    <Icon name='check'/>
                    SAFE!
                </div>);
            case 2:
                return (
                    <div style={{
                        color: 'red',
                        fontSize: '25px',
                        fontWeight: '1000'
                    }}>
                        <Icon name='x'/>
                        DANGER!
                    </div>
                );
            case 3:
                return (
                    <div style={{
                        color: 'darkorange',
                        fontSize: '25px',
                        fontWeight: '1000'
                    }}>
                        <Icon name='exclamation triangle'/>
                        PHISHING!
                    </div>
                );
        }
    };
  render() {
        const {loading, loaded, error} = this.state;
        const {subs, googleDatabase, amazonDatabase, whois, phishing, ssl, lastCheck, availableRate, frequent, total, collected, level, rating} = this.state;
    return (
      <div className="App">
        <header className="App-header" style={loaded?{minHeight: '20vh', maxHeight: '20vh', transition: 'all 1s'}:{transition: 'all 1s'}}>
            <div style={styles.layout}>
                <img src='logo.png' style={
                    loaded?{
                    width: `10%`,
                    height: `10%`,
                    transition: "all 1s",
                }:{transition: "all 1s",
                        width:"50%",
                        height: "50%"}} alt="logo" onClick={()=>{this.setState({loading: false, loaded: false})}} />
              <div style={styles.bar}>
                <Input fluid loading={loading} icon=
                    {loading?
                        null :
                        <Icon  name='search' inverted circular link
                               onClick={this.onSubmit.bind(this)}
                        />
                    }
                    placeholder='Input URL'
                       onChange={(event, data)=>{ this.setState({URL: data.value})}}
                       onKeyPress={(e)=>{if (e.key === 'Enter') this.onSubmit();}}
                       error={error}
                />
              </div>
            </div>
        </header>
          {loaded?
              <div style={{ margin: "10px auto", width: '95vw' }}>
                  <Segment placeholder>
                    <Grid columns={2} stackable>
                        <Grid.Row>
                            <Divider vertical> Summary </Divider>
                            <Grid.Column>
                                <Header icon>
                                    <Icon name='gem outline' />
                                    WatchFox Index
                                </Header>
                                {this.getLevel(level)}
                            </Grid.Column>

                            <Grid.Column>
                                <Header icon>
                                    <Icon name='comments outline' />
                                    Community Reputation
                                </Header>
                                <Rating onRate={this.onRate.bind(this)} maxRating={8} rating={rating} icon='star' size='massive'/>
                            </Grid.Column>
                        </Grid.Row>
                        <Divider/>
                        <Grid.Row>
                            {/*<textarea onChange={(e)=>{this.setState({markdown: e.target.value})}}/>*/}
                            <br/>
                            <div style={{display: 'flex', flexDirection:"column", alignItems:'flex-start', width: '90vw', margin: 'auto', textAlign:'left' , overflowY: 'hidden', overflowX: "scroll"}}>
                                {/*<Button onClick={()=>{*/}
                                    {/*this.setState({googleDatabase: "Passed!", amazonDatabase: "Passed!",*/}
                                    {/*})}}> Click Me!</Button>*/}
                            <ReactMarkdown source={`
## Blacklist History

### Google Database:

${googleDatabase || '<span class="lds-hourglass"></span>'}
<br/>
### Monapi Database:

${amazonDatabase|| '<span class="lds-hourglass"></span>' }

## WHOIS Information
<span style="text-align: left">
 ${ whois || '<span class="lds-hourglass"></span>' }
</span>

## Phishing Detection

 ${ phishing || '<span class="lds-hourglass"></span>' }

## SSL Certificate Information

 ${ ssl || '<span class="lds-hourglass"></span>' }


## Service Available Rate


| Item | Value |
| ---: | :---: |
| Last Check |  ${ lastCheck || '<span class="lds-hourglass"></span>' } |
| Rate | ${ availableRate || '<span class="lds-hourglass"></span>' } |
| Frequent | ${ frequent || '<span class="lds-hourglass"></span>' } |
| Total | ${ total || '<span class="lds-hourglass"></span>' } |
| Collected | ${ collected || '<span class="lds-hourglass"></span>' } |
`} escapeHtml={false}/>
                            </div>
                        </Grid.Row>
                    </Grid>
                  </Segment>

                  <div>
                      <Input placeholder={"EMail"} onChange={(d,v)=>{this.setState({email: v.value})}} />
                      <Button disabled={subs} primary={subs} onClick={()=>{this.state.socket.emit("subs", {email: this.state.email, url: this.state.URL}); this.setState({subs: true})}}> Subscribe </Button>
                  </div>
                  <div style={{color: 'gray'}}>
                      Proudly Provided By WatchFox
                  </div>
              </div>
              :""}
      </div>
    );
  }
}

export default App;
